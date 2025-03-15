# tasks\urls.py
from django.urls import path
from App_History import views


app_name = "App_History"


urlpatterns = [
    path("", views.history, name="history_page"),
]
