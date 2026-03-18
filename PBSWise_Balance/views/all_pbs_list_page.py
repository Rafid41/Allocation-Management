from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from ..models import PBS_List
from App_Login.models import User_Group

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
        # Partial search, case-insensitive
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
    """Handle adding a new PBS (Editor/Superuser only)."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to add.")
        return redirect("PBSWise_Balance:pbs_list_view")
    
    if request.method == "POST":
        pbs_name = request.POST.get('pbs_name', '').strip()
        if pbs_name:
            PBS_List.objects.create(pbs_name=pbs_name)
            messages.success(request, f"PBS '{pbs_name}' added successfully.")
        else:
            messages.error(request, "PBS Name cannot be empty.")
            
    return redirect("PBSWise_Balance:pbs_list_view")

def pbs_edit(request, pbs_id):
    """Handle editing an existing PBS (Editor/Superuser only)."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to edit.")
        return redirect("PBSWise_Balance:pbs_list_view")
    
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    if request.method == "POST":
        pbs_name = request.POST.get('pbs_name', '').strip()
        if pbs_name:
            pbs.pbs_name = pbs_name
            pbs.save()
            messages.success(request, f"PBS updated to '{pbs_name}'.")
        else:
            messages.error(request, "PBS Name cannot be empty.")
            
    return redirect("PBSWise_Balance:pbs_list_view")

def pbs_delete(request, pbs_id):
    """Handle deleting a PBS (Editor/Superuser only)."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to delete.")
        return redirect("PBSWise_Balance:pbs_list_view")
    
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    pbs_name = pbs.pbs_name
    pbs.delete()
    messages.success(request, f"PBS '{pbs_name}' deleted successfully.")
    return redirect("PBSWise_Balance:pbs_list_view")
