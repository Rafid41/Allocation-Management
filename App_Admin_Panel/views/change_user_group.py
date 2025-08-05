from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from App_Login.models import User_Group
from django.db.models import Q, OuterRef, Subquery
from django.contrib.auth.decorators import login_required

@login_required
def change_user_group_list_view(request):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")

    query = request.GET.get("q")

    # Subquery to get user_group_type from User_Group model
    user_group_subquery = User_Group.objects.filter(user=OuterRef('pk')).values('user_group_type')[:1]

    # Base queryset excluding superusers
    users = User.objects.filter(is_superuser=False).annotate(
        user_group_type=Subquery(user_group_subquery)
    )

    # Filter by search query if present
    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )

    # Sort by user_group_type
    users = users.order_by('user_group_type', 'username')

    # Build dictionary for display fallback if needed
    user_groups = {
        ug.user_id: ug.user_group_type
        for ug in User_Group.objects.filter(user__in=users)
    }

    context = {
        "users": users,
        "user_groups": user_groups,
        "search_query": query or "",
    }
    return render(request, "App_Admin_Panel/change_user_group_list.html", context)
