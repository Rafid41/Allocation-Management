from django.urls import path
from . import views

app_name = "App_Cancellation"

urlpatterns = [
    path("",views.cancellation_view, name="cancellation"),
]
