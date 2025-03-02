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


@login_required
def add_item_to_package(request):
    packages = Package.objects.all().order_by("packageId")
    items = Item.objects.all().order_by("package__packageId")

    UNIT_CHOICES = ["Nos.", "Mtr.", "Km.", "Set.", "Pair."]

    if request.method == "POST":
        package_id = request.POST.get("package")
        item_name = request.POST.get("item_name")
        warehouse = request.POST.get("warehouse")
        unit_of_item = request.POST.get("unit_of_item")
        unit_price = request.POST.get("unit_price")
        quantity_of_item = request.POST.get("quantity_of_item")
        description = request.POST.get("description")

        if unit_of_item not in UNIT_CHOICES:
            messages.error(request, "Invalid unit selected.")
            return redirect("App_Entry:add_item_to_package")

        package = get_object_or_404(Package, id=package_id)

        # Check if the same item already exists in the same warehouse
        existing_item = Item.objects.filter(name=item_name, package=package, warehouse=warehouse).first()

        if existing_item:
            if existing_item.quantity_of_item > 0:
                messages.error(
                    request,
                    f"Cannot update {item_name} in {warehouse} as it already exists with quantity {existing_item.quantity_of_item}.",
                )
                return redirect("App_Entry:add_item_to_package")

        # Add a new entry instead of updating if the warehouse is different
        Item.objects.create(
            name=item_name,
            package=package,
            warehouse=warehouse,
            unit_of_item=unit_of_item,
            unit_price=unit_price,
            quantity_of_item=quantity_of_item,
            description=description,
        )
        messages.success(
            request, f"Added {item_name} to package {package.packageId} in {warehouse} warehouse."
        )

        return redirect("App_Entry:add_item_to_package")

    return render(
        request,
        "App_Entry/Add_item_to_package.html",
        {"packages": packages, "items": items, "unit_choices": UNIT_CHOICES},
    )


@login_required
def delete_item(request, item_id):
    """Delete an existing item"""
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully!")
    return redirect("App_Entry:add_item_to_package")

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # Get the item by ID
    packages = Package.objects.all()

    if request.method == "POST":
        # Retrieve form data
        package_id = request.POST.get("package")
        item_name = request.POST.get("item_name")
        warehouse = request.POST.get("warehouse")
        unit_of_item = request.POST.get("unit_of_item")
        unit_price = request.POST.get("unit_price")
        quantity_of_item = request.POST.get("quantity_of_item")
        description = request.POST.get("description")

        # Validation
        if not all([package_id, item_name, warehouse, unit_of_item, unit_price, quantity_of_item]):
            messages.error(request, "All fields except description are required!")
            return redirect("App_Entry:edit_item", item_id=item.id)

        # Ensure unit_of_item is a valid choice key
        valid_units = dict(Item.UNIT_CHOICES).keys()
        if unit_of_item not in valid_units:
            messages.error(request, "Invalid unit selected!")
            return redirect("App_Entry:edit_item", item_id=item.id)

        # Check if the same item with the same warehouse exists with quantity > 0
        existing_item = Item.objects.filter(
            name=item_name, warehouse=warehouse
        ).exclude(id=item.id).first()

        if existing_item and existing_item.quantity_of_item > 0:
            messages.error(
                request,
                f"Cannot update '{item_name}' in '{warehouse}' as another entry exists with quantity {existing_item.quantity_of_item}.",
            )
            return redirect("App_Entry:edit_item", item_id=item.id)

        # Update item values
        item.package = get_object_or_404(Package, id=package_id)
        item.name = item_name
        item.warehouse = warehouse
        item.unit_of_item = unit_of_item  # Store only key (e.g., "Nos.", "Km.", etc.)
        item.unit_price = int(unit_price)
        item.quantity_of_item = int(quantity_of_item)
        item.description = description

        item.save()  # Save changes

        messages.success(request, "Item updated successfully!")
        return redirect("App_Entry:add_item_to_package")

    # Pass data to template
    return render(
        request,
        "App_Entry/edit_item.html",
        {
            "item": item,
            "packages": packages,
            "warehouse_choices": Item.WAREHOUSE_CHOICES,
            "unit_choices": Item.UNIT_CHOICES,
        },
    )
