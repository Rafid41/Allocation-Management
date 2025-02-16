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
    # path("package/", views.package_view, name="package"),
    # API endpoints
    # # Search APIs (for AJAX autocomplete)
    # path("search_packages/", views.search_packages, name="search_packages"),
    # path("search_items/", views.search_items, name="search_items"),
    # # Create or update package
    # path("create_package/", views.create_package, name="create_package"),
    # # Create or update package item
    # path("create_package_item/", views.create_package_item, name="create_package_item"),
]
