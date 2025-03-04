from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import PBS
from django.urls import reverse
from django.contrib import messages


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
# ########################  Search & Select for Allocation ##########################
from django.shortcuts import render
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime

def Search_and_Select(request):
    """Renders the package and item entry page with search functionality"""
    query = request.GET.get("query", "").strip()  # Strip leading/trailing whitespaces from query input
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
from django.shortcuts import render
from django.http import JsonResponse
from .models import Temporary_Allocation, PBS, Package, Item




def validate_allocation_no(request):
    """Check if the allocation number already exists."""
    allocation_no = request.GET.get("allocation_no")
    exists = Temporary_Allocation.objects.filter(allocation_no=allocation_no).exists()
    return JsonResponse({"exists": exists})


