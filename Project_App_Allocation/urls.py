# Project_App_Allocation\urls.py
from django.urls import path
from . import views

app_name = "Project_App_Allocation"

urlpatterns = [
    path("", views.allocation_page, name="allocation_page"),

    path(
        "view_PBS_and_addNew/",
        views.view_PBS_and_addNew,
        name="view_PBS_and_addNew",
    ),
    path("view_allocation_numbers/", views.view_allocation_numbers_and_Add_New, name="view_allocation_numbers_and_Add_New"),
    path('Search_and_Select/<int:allocation_id>/', views.Search_and_Select, name='Search_and_Select'),

    path('allocate_item/<int:allocation_id>/<int:item_id>/', views.allocate_item, name="allocate_item"),
    path("delete_allocation_in_allocate_page/<int:allocation_id>/", views.delete_allocation_in_allocate_page, name="delete_allocation_in_allocate_page"),

    path("final_allocation/", views.final_allocation_search, name="final_allocation"),
    path("delete_allocation_in_view_page/<int:allocation_id>/", views.delete_allocation_in_view_page, name="delete_allocation_in_view_page"),
    path("select_allocation_number/", views.select_allocation_number, name="select_allocation_number"),
    path('view_confirm_allocation/<int:allocation_id>/', views.view_confirm_allocation, name='view_confirm_allocation'),
    path('delete-all-allocations/<int:allocation_id>/', views.delete_all_allocations, name='delete_all_allocations'),
    path('confirm-allocation/<int:allocation_id>/', views.confirm_allocation, name='confirm_allocation'),
    path("final-allocation/individual-download/", views.individual_allocation_download, name="individual_final_allocation_download"),
]