from django.urls import path
from App_User_Group import views

app_name = "App_User_Group"

urlpatterns = [
    path("access-denied/", views.access_denied_view, name="access-denied"),
]
