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
    path('allocate_item/<int:item_id>/', views.allocate_item, name="allocate_item"),
    path('delete_allocation/<int:allocation_id>/', views.delete_allocation, name="delete_allocation"),
    path('confirm_allocation_view/', views.confirm_allocation_view, name="confirm_allocation_view"),
    path('confirm-allocation/<int:allocation_id>/', views.confirm_allocation, name='confirm_allocation'),
    path('view_final_allocation/', views.view_final_allocation, name='view_final_allocation'),
]