from django.urls import path
from . import views

app_name = "PBSWise_StoreWise_Balance"

urlpatterns = [
    path("storeWise_balance/", views.storewise_balance_home_view, name="storewise_balance_home"),
    path("storeWise_balance/<str:store_slug>/", views.store_detail_summary_view, name="store_detail_summary"),
]
