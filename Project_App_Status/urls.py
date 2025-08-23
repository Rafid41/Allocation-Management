# App_Status\urls.py
from django.urls import path
from . import views

app_name = "Project_App_Status"

urlpatterns = [
    # Page rendering
    path("", views.status_page, name="status_page"),
    path("update-comment/<int:id>/", views.update_comment, name="update_comment"),
]
