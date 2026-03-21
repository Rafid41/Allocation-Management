from django.urls import path
from .views import all_pbs_list_page, PBS_Zonals, manage_zonal_items, Zonal_Balance, zonal_details, individual_pbs_balance, individual_zonal_balance

app_name = "PBSWise_Balance"

urlpatterns = [
    path("pbswise_balance/pbs_list", all_pbs_list_page.pbs_list_view, name="pbs_list_view"),
    path("pbswise_balance/pbs_add", all_pbs_list_page.pbs_add, name="pbs_add"),
    path("pbswise_balance/pbs_edit/<uuid:pbs_id>", all_pbs_list_page.pbs_edit, name="pbs_edit"),
    path("pbswise_balance/pbs_delete/<uuid:pbs_id>", all_pbs_list_page.pbs_delete, name="pbs_delete"),
    
    # Zonal Items Management (Global)
    path("pbswise_balance/manage_zonal_home", manage_zonal_items.manage_zonal_home, name="manage_zonal_home"),
    path("pbswise_balance/manage_zonal_items", manage_zonal_items.manage_zonal_items, name="manage_zonal_items"),
    path("pbswise_balance/zonal_item_add", manage_zonal_items.zonal_item_add, name="zonal_item_add"),
    path("pbswise_balance/zonal_item_edit/<uuid:item_id>", manage_zonal_items.zonal_item_edit, name="zonal_item_edit"),
    path("pbswise_balance/zonal_item_delete/<uuid:item_id>", manage_zonal_items.zonal_item_delete, name="zonal_item_delete"),

    # Zonal Balance Management (Table-wise)
    path("pbswise_balance/Zonal_Balance", Zonal_Balance.zonal_balance_view, name="zonal_balance_view"),
    path("pbswise_balance/Zonal_Balance/add/", Zonal_Balance.zonal_balance_add, name="zonal_balance_add"),
    path("pbswise_balance/Zonal_Balance/edit/<uuid:record_id>/", Zonal_Balance.zonal_balance_edit, name="zonal_balance_edit"),
    path("pbswise_balance/Zonal_Balance/delete/<uuid:record_id>/", Zonal_Balance.zonal_balance_delete, name="zonal_balance_delete"),
    path("pbswise_balance/Zonal_Balance/get_zonals/", Zonal_Balance.get_zonals_by_pbs, name="get_zonals_by_pbs"),
    path("pbswise_balance/Zonal_Balance/check_unique/", Zonal_Balance.check_unique_zonal_balance, name="check_unique_zonal_balance"),

    # PBS Zonals
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/", PBS_Zonals.pbs_zonals_view, name="pbs_zonals_view"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/add/", PBS_Zonals.pbs_zonal_add, name="pbs_zonal_add"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/edit/<uuid:zonal_id>/", PBS_Zonals.pbs_zonal_edit, name="pbs_zonal_edit"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/delete/<uuid:zonal_id>/", PBS_Zonals.pbs_zonal_delete, name="pbs_zonal_delete"),
    
    # Zonal Details View-Only
    path("pbswise_balance/zonal_details/<uuid:zonal_id>/", zonal_details.zonal_details_view, name="zonal_details_view"),

    # Individual PBS Management
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/manage_individual_pbs_zonal_home/", individual_pbs_balance.manage_individual_pbs_zonal_home, name="manage_individual_pbs_zonal_home"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/manage_individual_pbs_zonal_items/", individual_pbs_balance.manage_individual_pbs_zonal_items, name="manage_individual_pbs_zonal_items"),

    # Regional Zonal Balance Management (Individual PBS)
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/manage_balance/", individual_zonal_balance.manage_balance_view, name="manage_balance_view"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/manage_balance/add/", individual_zonal_balance.manage_balance_add, name="manage_balance_add"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/manage_balance/edit/<uuid:record_id>/", individual_zonal_balance.manage_balance_edit, name="manage_balance_edit"),
    path("pbswise_balance/pbs_zonals/<uuid:pbs_id>/manage_balance/delete/<uuid:record_id>/", individual_zonal_balance.manage_balance_delete, name="manage_balance_delete"),
]
