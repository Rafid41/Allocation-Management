from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from App_Entry.models import Package, Item
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.urls import reverse


def entry_page(request):
    """Renders the package and item entry page"""
    return render(request, "App_Entry/entry_page.html")


from django.urls import reverse_lazy


##################################  view package and add new Package #################################
def view_package_and_addNew(request):
    """Handles both displaying the package list and adding a new package."""

    if request.method == "POST":
        package_id = request.POST.get("packageId", "").strip()  # Trim spaces

        if package_id:
            # Check if this packageId already exists
            if Package.objects.filter(packageId=package_id).exists():
                messages.error(request, "This package ID already exists!")
            else:
                Package.objects.create(packageId=package_id)
                messages.success(request, "Package added successfully!")
                return HttpResponseRedirect(
                    reverse("App_Entry:view_package_and_addNew")
                )
        else:
            messages.error(request, "Package ID cannot be empty.")

    # Fetch all packages with their items and sort by packageId, item name, and warehouse
    packages = Package.objects.all().order_by("packageId")
    items = Item.objects.select_related("package").order_by("package__packageId", "name", "warehouse")

    return render(
        request,
        "App_Entry/view_package_and_addNew.html",
        {"current_package_list": packages, "items": items},
    )



############################## Add New Item to a Package ##########################################

from django.utils.timezone import now


@login_required
def add_item_to_package(request):
    packages = Package.objects.all().order_by("packageId")
    items = Item.objects.all().order_by("package__packageId")

    # Fetch unique warehouses for the dropdown
    unique_warehouses = sorted(list(set(
        Item.objects.values_list('warehouse', flat=True).distinct()
    )))

    # Apply Dynamic Filters
    for i in range(1, 10):  # Supports up to 9 filters
        filter_type = request.GET.get(f"filter_type_{i}")
        filter_value = request.GET.get(f"filter_value_{i}")

        if filter_value:
            filter_value = filter_value.strip()

        # Skip empty or no-condition filters
        if not filter_type or filter_type == "no_condition" or not filter_value:
            continue

        # Apply filters based on type
        if filter_type == "package":
            items = items.filter(package__packageId__iexact=filter_value)
        elif filter_type == "item":
            items = items.filter(name__iexact=filter_value)
        elif filter_type == "warehouse":
            items = items.filter(warehouse__iexact=filter_value)

    UNIT_CHOICES =  [choice[0] for choice in Item.UNIT_CHOICES]

    if request.method == "POST":
        package_id = request.POST.get("package")
        item_name = request.POST.get("item_name")
        warehouse = request.POST.get("warehouse")
        unit_of_item = request.POST.get("unit_of_item")
        unit_price = request.POST.get("unit_price")
        quantity_of_item = request.POST.get("quantity_of_item")
        description = request.POST.get("description")
        created_at= request.POST.get("created_at")

        if unit_of_item not in UNIT_CHOICES:
            messages.error(request, "Invalid unit selected.")
            return redirect("App_Entry:add_item_to_package")

        package = get_object_or_404(Package, id=package_id)

        # Check if the same item exists in the same package
        existing_item = Item.objects.filter(name=item_name, package=package, warehouse=warehouse).first()

        if existing_item:
            if existing_item.quantity_of_item > 0:
                messages.error(
                    request,
                    f"Cannot update {item_name} in {warehouse} as it already exists with quantity {existing_item.quantity_of_item}.",
                )
                return redirect("App_Entry:add_item_to_package")

        # Check if the same package and item exist with a different price
        same_package_items = Item.objects.filter(name=item_name, package=package)
        price_updated = False

        if same_package_items.exists():
            for item in same_package_items:
                if item.unit_price != unit_price:
                    item.unit_price = unit_price
                    item.save()
                    price_updated = True

        # Add a new entry instead of updating if the warehouse is different
        Item.objects.create(
            name=item_name,
            package=package,
            warehouse=warehouse,
            unit_of_item=unit_of_item,
            unit_price=unit_price,
            quantity_of_item=quantity_of_item,
            description=description,
            created_at=created_at if created_at else now()

        )

        success_message = f"Added {item_name} to package {package.packageId} in {warehouse} warehouse."
        if price_updated:
            success_message += " Price updated for all matching entries."

        messages.success(request, success_message)

        return redirect("App_Entry:add_item_to_package")

    return render(
        request,
        "App_Entry/Add_item_to_package.html",
        {
            "packages": packages,
            "items": items,
            "unit_choices": UNIT_CHOICES,
            "unique_warehouses": unique_warehouses,
        },
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
        created_at = request.POST.get("created_at")

        # Validation
        if not all([package_id, item_name, warehouse, unit_of_item, unit_price, quantity_of_item]):
            messages.error(request, "All fields except description are required!")
            return redirect("App_Entry:edit_item", item_id=item.id)

        # Ensure unit_of_item is a valid choice key
        valid_units = dict(Item.UNIT_CHOICES).keys()
        if unit_of_item not in valid_units:
            messages.error(request, "Invalid unit selected!")
            return redirect("App_Entry:edit_item", item_id=item.id)

        # Check if warehouse has changed
        if warehouse != item.warehouse:
            # If warehouse is changed, ensure no other item with same name and warehouse exists with quantity > 0
            existing_item = Item.objects.filter(name=item_name, warehouse=warehouse).exclude(id=item.id).first()

            if existing_item and existing_item.quantity_of_item > 0:
                messages.error(
                    request,
                    f"Cannot update '{item_name}' to warehouse '{warehouse}' as another entry exists with quantity {existing_item.quantity_of_item}.",
                )
                return redirect("App_Entry:edit_item", item_id=item.id)

        # Check if the price has changed and update all entries with the same package and item
        new_price = unit_price
        if item.unit_price != new_price:
            Item.objects.filter(package_id=package_id, name=item_name).update(unit_price=new_price)
            messages.success(request, f"Price updated for all '{item_name}' in package '{package_id}'.")

        # Update item values
        item.package = get_object_or_404(Package, id=package_id)
        item.name = item_name
        item.warehouse = warehouse
        item.unit_of_item = unit_of_item  # Store only key (e.g., "Nos.", "Km.", etc.)
        item.unit_price = new_price
        item.quantity_of_item = quantity_of_item
        item.description = description
        item.created_at = created_at

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
