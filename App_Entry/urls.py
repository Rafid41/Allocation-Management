from django.urls import path
from . import views

app_name = "App_Entry"

urlpatterns = [
    # Page rendering
    path("", views.entry_page, name="entry_page"),
    path(
        "view_package_and_addNew/",
        views.view_package_and_addNew,
        name="view_package_and_addNew",
    ),
    path(
        "add_item_to_package/",
        views.add_item_to_pkg,
        name="add_item_to_package",
    ),
]
