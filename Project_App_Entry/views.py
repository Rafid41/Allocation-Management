from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from Project_App_Entry.models import Project, Project_Item
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.urls import reverse, reverse_lazy


def entry_page(request):
    """Renders the package and item entry page"""
    return render(request, "Project_Templates/Project_App_Entry/project_entry_page.html")






##################################  view project and add new Project #################################
def view_project_and_addNew(request):
    """Handles both displaying the project list and adding a new project."""

    if request.method == "POST":
        project_id = request.POST.get("projectId", "").strip()  # Trim spaces

        if project_id:
            # Check if this projectId already exists
            if Project.objects.filter(projectId=project_id).exists():
                messages.error(request, "This project ID already exists!")
            else:
                Project.objects.create(projectId=project_id)
                messages.success(request, "Project added successfully!")
                return HttpResponseRedirect(
                    reverse("Project_App_Entry:view_project_and_addNew")
                )
        else:
            messages.error(request, "Project ID cannot be empty.")

    # Fetch all projects with their items and sort by projectId, item name, and warehouse
    projects = Project.objects.all().order_by("projectId")
    items = Project_Item.objects.select_related("project").order_by("project__projectId", "name", "warehouse")

    return render(
        request,
        "Project_Templates/Project_App_Entry/view_project_and_addNew.html",
        {"current_project_list": projects, "items": items},
    )



############################## Add New Item to a Package ##########################################

from django.utils.timezone import now


@login_required
def add_item_to_project(request):
    projects = Project.objects.all().order_by("projectId")
    items = Project_Item.objects.all().order_by("project__projectId")

    UNIT_CHOICES = ["Nos.", "Mtr.", "Km.", "Set.", "Pair."]

    if request.method == "POST":
        project_id = request.POST.get("project")
        item_name = request.POST.get("item_name")
        warehouse = request.POST.get("warehouse")
        unit_of_item = request.POST.get("unit_of_item")
        # unit_price = request.POST.get("unit_price")
        quantity_of_item = int(request.POST.get("quantity_of_item"))
        description = request.POST.get("description")
        created_at= request.POST.get("created_at")

        if unit_of_item not in UNIT_CHOICES:
            messages.error(request, "Invalid unit selected.")
            return redirect("Project_App_Entry:add_item_to_project")

        project = get_object_or_404(Project, id=project_id)

        # Check if the same item exists in the same project
        existing_item = Project_Item.objects.filter(name=item_name, project=project, warehouse=warehouse).first()

        if existing_item:
            if existing_item.quantity_of_item > 0:
                messages.error(
                    request,
                    f"Cannot update {item_name} in {warehouse} as it already exists with quantity {existing_item.quantity_of_item}.",
                )
                return redirect("Project_App_Entry:add_item_to_project")

        # Check if the same project and item exist with a different price
        same_project_items = Project_Item.objects.filter(name=item_name, project=project)
        price_updated = False

        # if same_project_items.exists():
        #     for item in same_project_items:
        #         if item.unit_price != unit_price:
        #             item.unit_price = unit_price
        #             item.save()
        #             price_updated = True

        # Add a new entry instead of updating if the warehouse is different
        Project_Item.objects.create(
            name=item_name,
            project=project,
            warehouse=warehouse,
            unit_of_item=unit_of_item,
            # unit_price=unit_price,
            quantity_of_item=quantity_of_item,
            description=description,
            created_at=created_at if created_at else now()

        )

        success_message = f"Added {item_name} to project {project.projectId} in {warehouse} warehouse."
        if price_updated:
            success_message += " Price updated for all matching entries."

        messages.success(request, success_message)

        return redirect("Project_App_Entry:add_item_to_project")

    return render(
        request,
        "Project_Templates/Project_App_Entry/Add_item_to_project.html",
        {"projects": projects, "items": items, "unit_choices": UNIT_CHOICES},
    )

@login_required
def delete_item(request, item_id):
    """Delete an existing item"""
    item = get_object_or_404(Project_Item, id=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully!")
    return redirect("Project_App_Entry:add_item_to_project")



@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Project_Item, pk=item_id)  # Get the item by ID
    projects = Project.objects.all()

    if request.method == "POST":
        # Retrieve form data
        project_id = request.POST.get("project")
        item_name = request.POST.get("item_name")
        warehouse = request.POST.get("warehouse")
        unit_of_item = request.POST.get("unit_of_item")
        # unit_price = request.POST.get("unit_price")
        quantity_of_item = request.POST.get("quantity_of_item")
        description = request.POST.get("description")
        created_at = request.POST.get("created_at")

        # Validation
        if not all([project_id, item_name, warehouse, unit_of_item, quantity_of_item]):
            messages.error(request, "All fields except description are required!")
            return redirect("Project_App_Entry:edit_item", item_id=item.id)

        # Ensure unit_of_item is a valid choice key
        valid_units = dict(Project_Item.UNIT_CHOICES).keys()
        if unit_of_item not in valid_units:
            messages.error(request, "Invalid unit selected!")
            return redirect("Project_App_Entry:edit_item", item_id=item.id)

        # Check if warehouse has changed
        if warehouse != item.warehouse:
            # If warehouse is changed, ensure no other item with same name and warehouse exists with quantity > 0
            existing_item = Project_Item.objects.filter(name=item_name, warehouse=warehouse).exclude(id=item.id).first()

            if existing_item and existing_item.quantity_of_item > 0:
                messages.error(
                    request,
                    f"Cannot update '{item_name}' to warehouse '{warehouse}' as another entry exists with quantity {existing_item.quantity_of_item}.",
                )
                return redirect("Project_App_Entry:edit_item", item_id=item.id)


        # Update item values
        item.project = get_object_or_404(Project, id=project_id)
        item.name = item_name
        item.warehouse = warehouse
        item.unit_of_item = unit_of_item  # Store only key (e.g., "Nos.", "Km.", etc.)
        # item.unit_price = new_price
        item.quantity_of_item = int(quantity_of_item)
        item.description = description
        item.created_at = created_at

        item.save()  # Save changes

        messages.success(request, "Item updated successfully!")
        return redirect("Project_App_Entry:add_item_to_project")

    # Pass data to template
    return render(
        request,
        "Project_Templates/Project_App_Entry/edit_item.html",
        {
            "item": item,
            "projects": projects,
            "warehouse_choices": Project_Item.WAREHOUSE_CHOICES,
            "unit_choices": Project_Item.UNIT_CHOICES,
        },
    )
