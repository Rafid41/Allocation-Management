# App_Allocation\urls.py
from django.urls import path
from . import views

app_name = "App_Allocation"

urlpatterns = [
    path("", views.allocation_page, name="allocation_page"),
]
