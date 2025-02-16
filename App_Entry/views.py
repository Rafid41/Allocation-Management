import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from App_Entry.models import Package, Item
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    View,
    TemplateView,
    DeleteView,
)
from django import forms
from django.contrib import messages
from django.urls import reverse


def entry_page(request):
    """Renders the package and item entry page"""
    return render(request, "App_Entry/entry_page.html")


from django.urls import reverse_lazy


##################################  view package and add new Package #################################
@login_required
def view_package_and_addNew(request):
    """Handles both displaying the package list and adding a new package."""

    if request.method == "POST":
        package_id = request.POST.get("packageId")

        if package_id:
            # Ensure packageId is a valid integer
            try:
                package_id = int(package_id)
                if Package.objects.filter(packageId=package_id).exists():
                    messages.error(request, "This package ID already exists!")
                else:
                    Package.objects.create(packageId=package_id)
                    messages.success(request, "Package added successfully!")
                    return HttpResponseRedirect(
                        reverse("App_Entry:view_package_and_addNew")
                    )
            except ValueError:
                messages.error(request, "Invalid package ID. Please enter a number.")

    # Fetch all packages to display
    packages = Package.objects.all().order_by("packageId")

    return render(
        request,
        "App_Entry/view_package_and_addNew.html",
        {"current_package_list": packages},
    )


############################## Add New Item to a Package ##########################################

from django.utils.timezone import now


def add_item_to_package(request):
    packages = Package.objects.all().order_by(
        "packageId"
    )  # Ensuring packages are sorted
    items = Item.objects.all().order_by(
        "package__packageId"
    )  # Sorting items by package ID

    if request.method == "POST":
        package_id = request.POST.get("package")
        item_name = request.POST.get("item_name")
        warehouse = request.POST.get("warehouse")
        unit_of_item = request.POST.get("unit_of_item")
        unit_price = request.POST.get("unit_price")
        quantity_of_item = request.POST.get("quantity_of_item")
        description = request.POST.get("description")

        # Ensure package exists
        package = get_object_or_404(Package, id=package_id)

        # Check if item already exists within the package
        existing_item = Item.objects.filter(name=item_name, package=package).first()

        if existing_item:
            if existing_item.quantity_of_item > 0:
                messages.error(
                    request,
                    f"Cannot update {item_name} as it already exists with quantity {existing_item.quantity_of_item}.",
                )
                return redirect("App_Entry:add_item_to_package")

            # Update existing item
            existing_item.unit_of_item = unit_of_item
            existing_item.unit_price = unit_price
            existing_item.warehouse = warehouse
            existing_item.description = description
            existing_item.quantity_of_item = quantity_of_item  # Update quantity
            existing_item.save()
            messages.success(
                request, f"Updated {item_name} in package {package.packageId}."
            )

        else:
            # Create new item
            new_item = Item.objects.create(
                name=item_name,
                package=package,
                warehouse=warehouse,
                unit_of_item=unit_of_item,
                unit_price=unit_price,
                quantity_of_item=quantity_of_item,  # Added field
                description=description,
            )
            messages.success(
                request, f"Added {item_name} to package {package.packageId}."
            )

        return redirect("App_Entry:add_item_to_package")

    return render(
        request,
        "App_Entry/Add_item_to_package.html",
        {"packages": packages, "items": items},
    )
