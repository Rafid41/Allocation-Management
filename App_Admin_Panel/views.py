from django.shortcuts import render



from django.shortcuts import render, redirect

def admin_panel_home_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "App_Admin_Panel/admin_panel_home.html")

    else:
        return render(request, "App_User_Group/access_denied.html")

