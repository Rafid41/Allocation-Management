from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import PBS, Allocation_Number
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def allocation_page(request):
    """Renders the PBS and item entry page"""
    return render(request, "App_Allocation/allocation.html")


@login_required
def view_PBS_and_addNew(request):
    """Handles both displaying the PBS list and adding a new PBS."""

    if request.method == "POST":
        PBS_name = request.POST.get("PBS_Name")  # Fix: Match HTML form field name

        if PBS_name:
            PBS_name = PBS_name.strip()  # Remove extra spaces
            if PBS.objects.filter(name=PBS_name).exists():
                messages.error(
                    request, "This PBS already exists!"
                )  # Show error message
            else:
                PBS.objects.create(name=PBS_name)
                messages.success(
                    request, "PBS added successfully!"
                )  # Show success message
                return HttpResponseRedirect(
                    reverse("App_Allocation:view_PBS_and_addNew")
                )

    # Fetch all PBSs to display
    PBSs = PBS.objects.all().order_by("name")

    return render(
        request,
        "App_Allocation/view_PBS_and_addNew.html",
        {"current_PBS_list": PBSs},
    )


@login_required
def view_allocation_numbers_and_Add_New(request):
    """Handles both displaying the Allocation_Number list and adding a new one."""

    if request.method == "POST":
        allocation_no = request.POST.get("allocation_no")  # Get input from form

        if allocation_no:
            allocation_no = allocation_no.strip()  # Remove extra spaces
            if Allocation_Number.objects.filter(allocation_no=allocation_no).exists():
                messages.error(
                    request, "This Allocation Number already exists!"
                )  # Error message
            else:
                Allocation_Number.objects.create(allocation_no=allocation_no)
                messages.success(
                    request, "Allocation Number added successfully!"
                )  # Success message
                return redirect(
                    reverse("App_Allocation:view_allocation_numbers_and_Add_New")
                )

    # Fetch all allocation numbers to display
    allocation_numbers = Allocation_Number.objects.all().order_by("allocation_no")

    return render(
        request,
        "App_Allocation/view_allocation_numbers_and_Add_New.html",
        {"allocation_numbers": allocation_numbers},
    )


# ########################  Search & Select for Allocation ##########################
from django.shortcuts import render
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime


@login_required
def Search_and_Select(request):
    """Renders the package and item entry page with search functionality"""
    query = request.GET.get(
        "query", ""
    ).strip()  # Strip leading/trailing whitespaces from query input
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    items = Item.objects.all()

    # Apply query filter based on the selected 'filter_by' option
    if query:
        if filter_by == "All":
            items = items.filter(
                Q(name__icontains=query)
                | Q(package__packageId__icontains=query)
                | Q(warehouse__icontains=query)
                | Q(unit_of_item__icontains=query)
            )
        elif filter_by == "Package ID":
            items = items.filter(package__packageId__icontains=query)
        elif filter_by == "Item Name":
            items = items.filter(name__icontains=query)
        elif filter_by == "Warehouse":
            items = items.filter(warehouse__icontains=query)
        elif filter_by == "Unit":
            items = items.filter(unit_of_item__icontains=query)

    # Apply date filter only if "Entry/Update date" is selected
    if filter_by == "Entry/Update date" and date_filter:
        try:
            # Ensure the date format matches
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            items = items.filter(created_at__date=date_obj.date())
        except ValueError:
            pass  # If the date format is invalid, ignore the filter

    # Order the results by package ID
    items = items.order_by("package__packageId")

    return render(
        request,
        "App_Allocation/Search_and_Select.html",
        {
            "items": items,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
        },
    )


# ########################  Allocate to PBS ##########################
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Temporary_Allocation, Final_Allocation, PBS, Item, Allocation_Number
from .forms import TemporaryAllocationForm
from django.contrib.auth.decorators import login_required

def get_available_allocation_numbers():
    """
    Fetch allocation numbers that are not already in Final_Allocation, sorted in descending order.
    """
    final_allocations = Final_Allocation.objects.values_list("allocation_no", flat=True)
    return Allocation_Number.objects.exclude(id__in=final_allocations).order_by("-id")

@login_required
def allocate_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    pbss = PBS.objects.all()
    allocation_numbers = get_available_allocation_numbers()

    if request.method == "POST":
        form = TemporaryAllocationForm(request.POST)
        allocation_no_id = request.POST.get("allocation_no")
        pbs_id = request.POST.get("pbs")
        quantity = request.POST.get("quantity")

        # Convert quantity to integer safely
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity entered.")
            return redirect("App_Allocation:allocate_item", item_id=item.id)

        allocation_no = get_object_or_404(Allocation_Number, id=allocation_no_id)
        existing_allocations = Temporary_Allocation.objects.filter(
            allocation_no=allocation_no, item_primary_key=item.id
        )
        total_allocated = sum(existing.quantity for existing in existing_allocations)

        if total_allocated + quantity > item.quantity_of_item:
            messages.error(
                request, "Total allocated quantity exceeds available stock!"
            )
        elif not pbs_id:
            messages.error(request, "Please select a valid PBS before submitting.")
        else:
            allocation = form.save(commit=False)
            allocation.item = item
            allocation.item_primary_key = item.id
            allocation.package = item.package
            allocation.warehouse = item.warehouse
            allocation.price = item.unit_price
            allocation.pbs = get_object_or_404(PBS, id=pbs_id)
            allocation.allocation_no = allocation_no
            allocation.save()
            messages.success(request, "Item allocated successfully!")
            return redirect("App_Allocation:Search_and_Select")
    else:
        form = TemporaryAllocationForm()

    allocations = Temporary_Allocation.objects.all().order_by("-allocation_no")

    return render(
        request,
        "App_Allocation/allocate_item.html",
        {
            "form": form,
            "item": item,
            "pbss": pbss,
            "allocation_numbers": allocation_numbers,
            "allocations": allocations,
        },
    )

# ########################  Confirm Allocation ##########################

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from .models import Temporary_Allocation, Allocation_Number, Final_Allocation
from App_Entry.models import Item


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .models import Temporary_Allocation, Final_Allocation, Allocation_Number, Item
from django.contrib import messages
from django.shortcuts import redirect


def confirm_allocation_view(request):
    allocation_no = request.GET.get("query", "").strip()
    allocations = []

    if allocation_no.isdigit():  # Only search for numeric allocation numbers
        allocations = Temporary_Allocation.objects.filter(allocation_no__allocation_no=allocation_no)

    return render(request, "App_ALlocation/confirm_allocation.html", {"allocations": allocations, "query": allocation_no})



def confirm_allocation(request):
    """Render the Confirm Allocation page with search functionality."""
    query = request.GET.get("allocation_no", "").strip()
    allocations = []

    if query.isdigit():
        allocations = Temporary_Allocation.objects.filter(allocation_no__allocation_no=query)

    return render(request, "App_Allocation/confirm_allocation.html", {
        "allocations": allocations,
        "query": query,
    })

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_allocation(request, allocation_no):
    if request.method == "DELETE":
        try:
            allocations = Temporary_Allocation.objects.filter(allocation_no__allocation_no=allocation_no)
            if allocations.exists():
                allocations.delete()
                return JsonResponse({"message": "Allocation deleted successfully"}, status=200)
            else:
                return JsonResponse({"error": "Allocation not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def process_allocation(request):
    """Process and confirm allocations, moving them from Temporary to Final_Allocation."""
    if request.method == "POST":
        allocation_no = request.POST.get("allocation_no")
        allocations = Temporary_Allocation.objects.filter(allocation_no__allocation_no=allocation_no)

        if not allocations.exists():
            return JsonResponse({"success": False, "message": "No allocations found."})

        item_sums = {}

        # Calculate total allocated quantity per item
        for alloc in allocations:
            if alloc.item_primary_key not in item_sums:
                item_sums[alloc.item_primary_key] = 0
            item_sums[alloc.item_primary_key] += alloc.quantity

        # Validate available item stock
        errors = []
        for item_pk, allocated_qty in item_sums.items():
            item = Item.objects.get(id=item_pk)
            if allocated_qty > item.quantity_of_item:
                errors.append(f"{item.name} exceeds available limit")

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        # If valid, process allocation
        with transaction.atomic():
            for alloc in allocations:
                item = alloc.item
                item.quantity_of_item -= alloc.quantity
                item.save()

                Final_Allocation.objects.create(
                    allocation_no=alloc.allocation_no,
                    item_primary_key=alloc.item_primary_key,
                    pbs=alloc.pbs,
                    package=alloc.package,
                    item=alloc.item,
                    warehouse=alloc.warehouse,
                    quantity=alloc.quantity,
                    price=alloc.price,
                )

            allocations.delete()

        return JsonResponse({"success": True, "message": "Allocation confirmed successfully."})

    return JsonResponse({"success": False, "message": "Invalid request."})


# ########################  Search & Print for Final Allocation ##########################
from django.shortcuts import render
from App_Allocation.models import Final_Allocation
from django.db.models import Q
from datetime import datetime


def view_final_allocation(request):
    """Renders the Final Allocation search and print page"""

    query = request.GET.get("query", "").strip()
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    allocations = Final_Allocation.objects.all()

    # Apply query filter based on the selected 'filter_by' option
    if query:
        if filter_by == "All":
            allocations = allocations.filter(
                Q(allocation_no__icontains=query)
                | Q(pbs__name__icontains=query)  # Assuming PBS has a 'name' field
                | Q(package__packageId__icontains=query)
                | Q(item__name__icontains=query)
                | Q(warehouse__icontains=query)
            )
        elif filter_by == "Allocation No":
            allocations = allocations.filter(allocation_no__icontains=query)
        elif filter_by == "PBS":
            allocations = allocations.filter(pbs__name__icontains=query)
        elif filter_by == "Package":
            allocations = allocations.filter(package__packageId__icontains=query)
        elif filter_by == "Item":
            allocations = allocations.filter(item__name__icontains=query)
        elif filter_by == "Warehouse":
            allocations = allocations.filter(warehouse__icontains=query)

    # Apply date filter
    if filter_by == "Entry/Update date" and date_filter:
        try:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            allocations = allocations.filter(created_at__date=date_obj.date())
        except ValueError:
            pass  # Ignore invalid date formats

    # Order by allocation_no
    allocations = allocations.order_by("allocation_no")

    return render(
        request,
        "App_Allocation/view_print_Final_allocation.html",
        {
            "allocations": allocations,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
        },
    )
