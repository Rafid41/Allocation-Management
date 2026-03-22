from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def storewise_balance_home_view(request):
    """
    Authorized home view for regional Storewise Balance analysis.
    Restricted to Superusers and Editors for professional auditing.
    """
    if not request.user.is_superuser and getattr(request.user.user_group, 'user_group_type', '') != "Editor":
        return redirect("App_User_Group:access-denied")

    return render(request, "PBSWise_Templates/PBSWise_StoreWise_Balance/storewise_balance_home.html")
