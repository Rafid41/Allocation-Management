from django.urls import path
from Project_Apps.App_Project_Home import views


app_name = "Project_Apps.App_Project_Home"


urlpatterns = [
    path("", views.home, name="project_home_page"),
]