from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "App_Home/home_page.html")
