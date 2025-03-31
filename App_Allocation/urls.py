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
    path("view_allocation_numbers/", views.view_allocation_numbers_and_Add_New, name="view_allocation_numbers_and_Add_New"),
    # path('Search_and_Select/<int:allocation_id>/', views.Search_and_Select, name='Search_and_Select'),
    path('Search_and_Select/<int:allocation_id>/', views.Search_and_Select, name='Search_and_Select'),

    path('allocate_item/<int:allocation_id>/<int:item_id>/', views.allocate_item, name="allocate_item"),
    path("delete_allocation_in_allocate_page/<int:allocation_id>/", views.delete_allocation_in_allocate_page, name="delete_allocation_in_allocate_page"),

###########################
    path("confirm_allocation/", views.confirm_allocation_view, name="confirm_allocation"),  # Fixed path name
    path("delete_allocation/<int:allocation_no>/", views.delete_allocation, name="delete_allocation"),
    path("confirm_allocation_process/<int:allocation_no>/", views.confirm_allocation, name="confirm_allocation_process"),  # Unique name
    path("final_allocation/", views.final_allocation_search, name="final_allocation"),
    
    path("generate-report/", views.generate_report, name="generate_report"),
    path("select_allocation_number/", views.select_allocation_number, name="select_allocation_number"),
]