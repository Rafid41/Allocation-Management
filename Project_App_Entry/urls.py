from django.urls import path
from . import views

app_name = "Project_App_Entry"

urlpatterns = [
    # Page rendering
    path("", views.entry_page, name="entry_page"),
#     path(
#         "view_package_and_addNew/",
#         views.view_package_and_addNew,
#         name="view_package_and_addNew",
#     ),
#     path(
#         "add_item_to_package/",
#         views.add_item_to_package,
#         name="add_item_to_package",
#     ),
#     path("edit-item/<int:item_id>/", views.edit_item, name="edit_item"),
#     path("delete-item/<int:item_id>/", views.delete_item, name="delete_item"),
]
