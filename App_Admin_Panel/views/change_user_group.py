from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from App_Login.models import User_Group
from django.db.models import Q, OuterRef, Subquery
from django.contrib.auth.decorators import login_required

@login_required
def change_user_group_list_view(request):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")

    query = request.GET.get("q")
    user_group_subquery = User_Group.objects.filter(user=OuterRef('pk')).values('user_group_type')[:1]
    users = User.objects.filter(is_superuser=False).annotate(
        user_group_type=Subquery(user_group_subquery)
    )

    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )

    users = users.order_by('user_group_type', 'username')
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






@login_required
def change_user_group_view(request, user_id):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")

    user = get_object_or_404(User, pk=user_id, is_superuser=False)


    user_group, created = User_Group.objects.get_or_create(user=user)

    if request.method == "POST":
        new_group_type = request.POST.get("user_group_type")
        if new_group_type in dict(User_Group.STATUS_CHOICES):
            user_group.user_group_type = new_group_type
            user_group.save()
            return redirect("App_Admin_Panel:change_user_group")

    context = {
        "user": user,
        "user_group": user_group,
        "status_choices": User_Group.STATUS_CHOICES,
    }
    return render(request, "App_Admin_Panel/change_user_group.html", context)

