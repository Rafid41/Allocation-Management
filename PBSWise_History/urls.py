from django.urls import path
from . import views

app_name = "PBSWise_History"

urlpatterns = [
    path("pbswise_history/", views.pbswise_history_view, name="pbswise_history"),
    path("history_suggestions_ajax/", views.get_history_suggestions_ajax, name="history_suggestions_ajax"),
    path("export_history_docx/", views.export_history_docx, name="export_history_docx"),
]
