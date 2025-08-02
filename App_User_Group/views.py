from django.shortcuts import render

def access_denied_view(request):
    return render(request, "App_User_Group/access_denied.html")
