from django.urls import path
from App_Admin_Panel import views

app_name = "App_Admin_Panel"

urlpatterns = [
    path("admin_panel_home/", views.admin_panel_home_view, name="admin_panel_home"),
]
