from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from App_Admin_Panel.models import PaginationManager

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def manage_pagination_view(request):
    config = PaginationManager.load()
    if request.method == "POST":
        try:
            limit = int(request.POST.get("pagination_limit"))
            if limit < 1:
                messages.error(request, "Pagination limit must be at least 1.")
            else:
                config.table_pagination_limit = limit
                config.save()
                messages.success(request, f"Pagination limit set to {limit}.")
                return redirect("App_Admin_Panel:admin_panel_home")
        except ValueError:
            messages.error(request, "Invalid input. Please enter a valid number.")

    context = {
        "current_limit": config.table_pagination_limit
    }
    return render(request, "App_Admin_Panel/manage_pagination.html", context)
