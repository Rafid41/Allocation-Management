from django.urls import path
from . import views

app_name = "Project_App_ProjectWiseBalance"

urlpatterns = [
    path('projects/', views.project_list, name="project_list"),
    path('project_details/<int:project_id>/', views.project_details, name="project_details"),
     path(
        "projects/project_details/update-remarks/<int:item_id>/",
        views.update_remarks,
        name="update_remarks",
    ),
]
