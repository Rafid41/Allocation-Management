# App_Status\urls.py
from django.urls import path
from . import views

app_name = "App_Status"

urlpatterns = [
    # Page rendering
    path("", views.status_page, name="status_page"),

]
