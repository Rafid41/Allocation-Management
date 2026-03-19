from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from App_Login.models import User_Group
from PBSWise_Balance.models import PBS_List
from PBSWise_Balance.views.all_pbs_list_page import generate_pbs_password, get_pbs_username

@login_required
def manage_pbs_accounts_view(request):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")

    pbs_list = PBS_List.objects.all().order_by('pbs_name')
    pbs_accounts = []

    for pbs in pbs_list:
        username = get_pbs_username(pbs.pbs_name)
        try:
            user = User.objects.get(username=username)
            user_group = User_Group.objects.get(user=user)
            pbs_accounts.append({
                'pbs_name': pbs.pbs_name,
                'user': user,
                'cleartext_password': user_group.cleartext_password or "Not Recorded",
            })
        except (User.DoesNotExist, User_Group.DoesNotExist):
            # If account is missing, maybe it wasn't sync'd yet.
            # We can skip or show a 'Create' button. 
            # For now, we only show existing ones.
            pass

    return render(request, "App_Admin_Panel/manage_pbs_accounts.html", {'pbs_accounts': pbs_accounts})

@login_required
def change_pbs_password_view(request, user_id):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")

    user = get_object_or_404(User, id=user_id)
    user_group = get_object_or_404(User_Group, user=user)

    if request.method == "POST":
        new_password = generate_pbs_password()
        user.set_password(new_password)
        user.save()
        user_group.cleartext_password = new_password
        user_group.save()
        messages.success(request, f"Password for '{user.username}' has been regenerated and updated.")
        return redirect("App_Admin_Panel:manage_pbs_accounts")

    return redirect("App_Admin_Panel:manage_pbs_accounts")
