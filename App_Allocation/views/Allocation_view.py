# ########################  Search & Select for Allocation ##########################
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from App_Allocation.models import Allocation_Number, Final_Allocation

@login_required
def select_allocation_number(request):
    """Display dropdown of allocation numbers filtered by current user and excluding ones in Final_Allocation."""
    
    # Get current user's allocation numbers
    user_allocations = Allocation_Number.objects.filter(user=request.user)
    
    # Get allocation numbers already in Final_Allocation
    final_allocations = Final_Allocation.objects.values_list('allocation_no_id', flat=True)

    # Exclude the ones already in Final_Allocation
    filtered_allocations = user_allocations.exclude(id__in=final_allocations).order_by("-allocation_no")

    if request.method == "POST":
        allocation_id = request.POST.get("allocation_no")
        if allocation_id:
            return redirect(reverse("App_Allocation:Search_and_Select", args=[allocation_id]))

    return render(
        request,
        "App_Allocation/select_allocation_number.html",
        {"allocation_numbers": filtered_allocations},
    )

@login_required
def Search_and_Select(request, allocation_id=None):
    """Renders the package and item entry page with search functionality and shows the allocation number if provided."""
    query = request.GET.get("query", "").strip()  
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
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            items = items.filter(created_at__date=date_obj.date())
        except ValueError:
            pass  

    # Order the results by package ID
    items = items.order_by("package__packageId")

    # Fetch Allocation Number if provided
    allocation_number = None
    if allocation_id:
        try:
            allocation = Allocation_Number.objects.get(id=allocation_id)
            allocation_number = allocation.allocation_no
        except Allocation_Number.DoesNotExist:
            messages.error(request, "Invalid Allocation Number.")

    return render(
        request,
        "App_Allocation/Search_and_Select.html",
        {
            "items": items,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
            "allocation_number": allocation_number,
            "allocation_id": allocation_id,
        },
    )


# ########################  Allocate to PBS ##########################
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from App_Allocation.models import Temporary_Allocation, Final_Allocation, PBS, Item, Allocation_Number
from App_Allocation.forms import TemporaryAllocationForm
from django.contrib.auth.decorators import login_required




@login_required
def allocate_item(request, allocation_id, item_id):
    item = get_object_or_404(Item, id=item_id)
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    pbss = PBS.objects.all()

    if request.method == "POST":
        form = TemporaryAllocationForm(request.POST)
        pbs_id = request.POST.get("pbs")
        quantity = request.POST.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity entered.")
            return redirect("App_Allocation:allocate_item", allocation_no=allocation_id, item_id=item.id)

        existing_allocations = Temporary_Allocation.objects.filter(
            allocation_no=allocation_no_obj, item_primary_key=item.id
        )
        total_allocated = sum(existing.quantity for existing in existing_allocations)

        # if total_allocated + quantity > item.quantity_of_item:
        if quantity > item.quantity_of_item:
            messages.error(request, "Total allocated quantity exceeds available stock!")
        elif quantity == 0:
            messages.error(request, "Quantity cannot be zero.")
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
            allocation.allocation_no = allocation_no_obj
            allocation.unit_of_item = item.unit_of_item

            # Ensure item has enough stock before saving allocation
            if item.quantity_of_item >= quantity:
                allocation.save()
                # Subtract allocated quantity from item stock
                item.quantity_of_item -= quantity
                item.save()
                messages.success(request, "Item allocated successfully!")
            else:
                messages.error(request, "Not enough stock available for allocation.")

            return redirect("App_Allocation:Search_and_Select", allocation_id=allocation_id)

    else:
        form = TemporaryAllocationForm()

    allocations = Temporary_Allocation.objects.filter(allocation_no=allocation_no_obj).order_by("-created_at")

    return render(
        request,
        "App_Allocation/allocate_item.html",
        {
            "form": form,
            "item": item,
            "allocation_no_obj": allocation_no_obj,
            "pbss": pbss,
            "allocations": allocations,
        },
    )


@login_required
def delete_allocation_in_allocate_page(request, allocation_id):
    allocation = get_object_or_404(Temporary_Allocation, id=allocation_id)
    item = get_object_or_404(Item, id=allocation.item_primary_key)

    if request.method == "POST":
        # Add back the allocated quantity to the Item stock
        item.quantity_of_item += allocation.quantity
        item.save()
        
        # Delete the allocation entry
        allocation.delete()
        
        messages.success(request, "Allocation entry deleted successfully.")
        return redirect("App_Allocation:allocate_item", allocation_id=allocation.allocation_no.id, item_id=item.id)

    return redirect("App_Allocation:allocate_item", allocation_id=allocation.allocation_no.id, item_id=item.id)
