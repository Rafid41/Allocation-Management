from django.urls import path
from . import views

app_name = "Project_App_Modification"

urlpatterns = [
    path('', views.modification_view, name="modification_menu"),
    path("modification-options/<int:allocation_id>/", views.modification_options, name="modification_options"),
    path('view-final-allocation/<int:allocation_id>/', views.view_final_allocation, name='view_final_allocation'),
    path('delete-final-allocation-entry/<int:allocation_id>/', views.delete_final_allocation_entry, name='delete_final_allocation_entry'),
    path('search_and_select_item/<int:allocation_id>/', views.Search_and_Select_Items, name='search_and_select_item'),
    path('add_item/<int:allocation_id>/<int:item_id>/', views.add_item, name='add_item'),
]
