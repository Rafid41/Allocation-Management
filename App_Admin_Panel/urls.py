from django.urls import path
from App_Admin_Panel import views

app_name = "App_Admin_Panel"

urlpatterns = [
    path("admin_panel_home/", views.admin_panel_home_view, name="admin_panel_home"),
    path("add-user/", views.add_new_user_view, name="add_new_user"),
    path("assign-user-group/<int:user_id>/", views.assign_user_group_view, name="assign_user_group"),
    path('change-user-group/', views.change_user_group_list_view, name='change_user_group'),
]
