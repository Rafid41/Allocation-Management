# App_Allocation\urls.py
from django.urls import path
from . import views

app_name = "App_Allocation"

urlpatterns = [
    path("", views.allocation_page, name="allocation_page"),
    path(
        "view_PBS_and_addNew/",
        views.view_PBS_and_addNew,
        name="view_PBS_and_addNew",
    ),
    path('Search_and_Select/', views.Search_and_Select, name='Search_and_Select'),
]