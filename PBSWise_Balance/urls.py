from django.urls import path
from .views import all_pbs_list_page

app_name = "PBSWise_Balance"

urlpatterns = [
    path("pbswise_balance/pbs_list", all_pbs_list_page.pbs_list_view, name="pbs_list_view"),
    path("pbswise_balance/pbs_add", all_pbs_list_page.pbs_add, name="pbs_add"),
    path("pbswise_balance/pbs_edit/<uuid:pbs_id>", all_pbs_list_page.pbs_edit, name="pbs_edit"),
    path("pbswise_balance/pbs_delete/<uuid:pbs_id>", all_pbs_list_page.pbs_delete, name="pbs_delete"),
]
