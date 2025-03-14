# ########################  Search & Select for Allocation ##########################
from django.shortcuts import render
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required

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
from App_Allocation.models import Temporary_Allocation, Final_Allocation, PBS, Item, Allocation_Number
from App_Allocation.forms import TemporaryAllocationForm
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
