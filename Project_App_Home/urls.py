from django.urls import path
from Project_App_Home import views


app_name = "Project_App_Home"


urlpatterns = [
    path("", views.home, name="project_home_page"),
]