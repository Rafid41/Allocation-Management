from django.urls import path
from .views import pbs_lists

app_name = "PBSWise_Inventory"

urlpatterns = [
    path("inventory/pbs_list", pbs_lists.pbs_list_view, name="pbs_list_view"),
]
