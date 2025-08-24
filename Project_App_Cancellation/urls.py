from django.urls import path
from . import views

app_name = "Project_App_Cancellation"

urlpatterns = [
    path("",views.cancellation_view, name="cancellation"),
]
