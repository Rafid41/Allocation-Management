from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "Project_Templates/Project_Home/project_home_page.html")
