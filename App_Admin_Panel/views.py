from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.contrib import messages
from App_Login.models import User_Group
from .forms import CustomUserCreationForm

def admin_panel_home_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "App_Admin_Panel/admin_panel_home.html")
    else:
        return render(request, "App_User_Group/access_denied.html")





def add_new_user_view(request):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            messages.success(request, f"User {user.username} created successfully.")
            return redirect("App_Admin_Panel:assign_user_group", user_id=user.id)
    else:
        form = CustomUserCreationForm()
    
    return render(request, "App_Admin_Panel/add_new_user.html", {"form": form})


def assign_user_group_view(request, user_id):
    if not request.user.is_superuser:
        return redirect("App_User_Group:access_denied")


    user = User.objects.get(id=user_id)

    if request.method == "POST":
        group_type = request.POST.get("user_group_type")
        User_Group.objects.create(user=user, user_group_type=group_type)
        messages.success(request, f"User group assigned to {user.username}.")
        return redirect("App_Admin_Panel:admin_panel_home")

    return render(request, "App_Admin_Panel/assign_user_group.html", {
        "user": user,
        "group_choices": User_Group.STATUS_CHOICES,
    })
