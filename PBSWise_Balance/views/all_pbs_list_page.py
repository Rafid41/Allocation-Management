from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ..models import PBS_List
from App_Login.models import User_Group

import string
import random
from django.contrib.auth.models import User

def generate_pbs_password():
    """Generates a random 10-char password with specific requirements."""
    length = 10
    specials = "!@#$%^&*"
    chars_upper = string.ascii_uppercase
    chars_lower = string.ascii_lowercase
    chars_digits = string.digits
    
    # Requirement: min 1 cap, 1 small, 1 digit, 1 special
    password = [
        random.choice(chars_upper),
        random.choice(chars_lower),
        random.choice(chars_digits),
        random.choice(specials)
    ]
    
    # Fill remaining 6 chars
    all_chars = chars_upper + chars_lower + chars_digits + specials
    password += [random.choice(all_chars) for _ in range(length - 4)]
    
    random.shuffle(password)
    return "".join(password)

def get_pbs_username(pbs_name):
    """Formats PBS name into breb-pbs-<TrimmedName>."""
    clean_name = "".join(pbs_name.split())
    return f"breb-pbs-{clean_name}"

def check_editor_permission(user):
    """Helper function to check if user has editor/superuser permissions."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        user_group = User_Group.objects.get(user=user)
        return user_group.user_group_type == "Editor"
    except User_Group.DoesNotExist:
        return False

def pbs_list_view(request):
    """View to list all PBS items with search and CRUD options."""
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        pbs_items = PBS_List.objects.filter(pbs_name__icontains=search_query).order_by('pbs_name')
    else:
        pbs_items = PBS_List.objects.all().order_by('pbs_name')
    
    is_editor = check_editor_permission(request.user)
    
    context = {
        'pbs_items': pbs_items,
        'search_query': search_query,
        'is_editor': is_editor,
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/all_pbs_list_page.html", context)

def pbs_add(request):
    """Handle adding a new PBS (Editor/Superuser only) + Create Account."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to add.")
        return redirect("PBSWise_Balance:pbs_list_view")
    
    if request.method == "POST":
        pbs_name = request.POST.get('pbs_name', '').strip()
        if pbs_name:
            # Check for duplicate: case-insensitive and trimmed (via .strip() and __iexact)
            if PBS_List.objects.filter(pbs_name__iexact=pbs_name).exists():
                messages.error(request, "This PBS Already Exists")
                return redirect("PBSWise_Balance:pbs_list_view")

            # Create PBS Entry
            PBS_List.objects.create(pbs_name=pbs_name)
            
            # Create Associated Account
            username = get_pbs_username(pbs_name)
            password = generate_pbs_password()
            
            # Check if username already exists to avoid conflict
            if not User.objects.filter(username=username).exists():
                new_user = User.objects.create_user(username=username, password=password)
                User_Group.objects.create(
                    user=new_user, 
                    user_group_type="Specific_PBS_Account",
                    cleartext_password=password
                )
                messages.success(request, f"PBS and corresponding Account '{username}' added successfully.")
            else:
                messages.success(request, f"PBS added, but account '{username}' already exists.")
        else:
            messages.error(request, "PBS Name cannot be empty.")
            
    return redirect("PBSWise_Balance:pbs_list_view")

def pbs_edit(request, pbs_id):
    """Handle editing an existing PBS (Editor/Superuser only) + Update Username."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to edit.")
        return redirect("PBSWise_Balance:pbs_list_view")
    
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    old_username = get_pbs_username(pbs.pbs_name)
    
    if request.method == "POST":
        pbs_name = request.POST.get('pbs_name', '').strip()
        if pbs_name:
            # Check for duplicate: case-insensitive and trimmed (excluding current pbs)
            if PBS_List.objects.filter(pbs_name__iexact=pbs_name).exclude(id=pbs.id).exists():
                messages.error(request, "This PBS Already Exists")
                return redirect("PBSWise_Balance:pbs_list_view")

            new_username = get_pbs_username(pbs_name)
            
            # Update PBS name
            pbs.pbs_name = pbs_name
            pbs.save()
            
            # Update User username and password if it exists
            try:
                user = User.objects.get(username=old_username)
                new_password = generate_pbs_password()
                user.username = new_username
                user.set_password(new_password)
                user.save()
                
                # Update cleartext password in User_Group
                user_group, _ = User_Group.objects.get_or_create(user=user)
                user_group.cleartext_password = new_password
                user_group.save()
                
                messages.success(request, f"PBS and account '{new_username}' updated (Name & Password).")
            except User.DoesNotExist:
                # If user didn't exist, create it now for the new name
                password = generate_pbs_password()
                new_user = User.objects.create_user(username=new_username, password=password)
                User_Group.objects.create(
                    user=new_user, 
                    user_group_type="Specific_PBS_Account",
                    cleartext_password=password
                )
                messages.success(request, f"PBS updated and new account '{new_username}' created.")
        else:
            messages.error(request, "PBS Name cannot be empty.")
            
    return redirect("PBSWise_Balance:pbs_list_view")

def pbs_delete(request, pbs_id):
    """Handle deleting a PBS (Editor/Superuser only) + Delete Account."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to delete.")
        return redirect("PBSWise_Balance:pbs_list_view")
    
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    username = get_pbs_username(pbs.pbs_name)
    pbs_name = pbs.pbs_name
    
    # Delete PBS entry
    pbs.delete()
    
    # Delete associated user if exists
    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, f"PBS and associated account '{username}' deleted successfully.")
    except User.DoesNotExist:
        messages.success(request, f"PBS '{pbs_name}' deleted.")
        
    return redirect("PBSWise_Balance:pbs_list_view")
