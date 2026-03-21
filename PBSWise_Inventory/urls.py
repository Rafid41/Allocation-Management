from django.urls import path
from .views import pbs_lists, inventory_management

app_name = "PBSWise_Inventory"

urlpatterns = [
    path("inventory/pbs_list", pbs_lists.pbs_list_view, name="pbs_list_view"),
    path("inventory/pbs/<uuid:pbs_id>/manage/", inventory_management.inventory_management_view, name="inventory_management_view"),
    path("inventory/ajax/get_items_for_zonal/", inventory_management.get_items_for_zonal_ajax, name="get_items_for_zonal_ajax"),
]
