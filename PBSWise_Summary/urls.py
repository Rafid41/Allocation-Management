from django.urls import path
from . import views

app_name = "PBSWise_Summary"

urlpatterns = [
    path("PBS_Summary/", views.pbswise_summary_view, name="pbs_summary"),
    path("get_summary_suggestions_ajax/", views.get_summary_suggestions_ajax, name="summary_suggestions_ajax"),
]
