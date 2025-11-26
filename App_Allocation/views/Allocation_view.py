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
    
    all_items = Item.objects.all()
    
    # Store active filters and queries to pass back to the template
    active_filters = {}
    
    # Start with an empty Q object for dynamic filtering
    combined_q = Q()
    
    # Loop through potential filter parameters (up to 5, as per JS maxFilterRows)
    for i in range(5): 
        filter_by_key = f"filter_by_{i}"
        query_key = f"query_{i}"
        
        filter_by = request.GET.get(filter_by_key, "").strip()
        query = request.GET.get(query_key, "").strip()
        
        if filter_by and filter_by != "No Condition":
            active_filters[filter_by_key] = filter_by
            active_filters[query_key] = query
            
            if query: # Only apply query if there's a value
                if filter_by == "Package ID":
                    combined_q &= Q(package__packageId__iexact=query)
                elif filter_by == "Item Name":
                    combined_q &= Q(name__iexact=query)
                elif filter_by == "Warehouse":
                    combined_q &= Q(warehouse__iexact=query)
                elif filter_by == "Entry/Update Date": # Changed from "Entry/Update date" to match instructions
                    try:
                        date_obj = datetime.strptime(query, "%Y-%m-%d")
                        combined_q &= Q(created_at__date=date_obj.date())
                    except ValueError:
                        # If date format is invalid, the filter for this date is ignored
                        pass
    
    # Apply the combined filters to the queryset
    if combined_q:
        all_items = all_items.filter(combined_q)

    # Order the results by Item Name
    all_items = all_items.order_by("name")

    # Get warehouse choices from the Item model
    all_possible_warehouses = [choice[0] for choice in Item.WAREHOUSE_CHOICES]

    # Fetch Allocation Number if provided
    allocation_number = None
    if allocation_id:
        try:
            allocation = Allocation_Number.objects.get(id=allocation_id)
            allocation_number = allocation.allocation_no
        except Allocation_Number.DoesNotExist:
            messages.error(request, "Invalid Allocation Number.")

    context = {
        "items": all_items,
        "allocation_number": allocation_number,
        "allocation_id": allocation_id,
        "unique_warehouses": all_possible_warehouses,
    }
    context.update(active_filters) # Add active filters back to context for template

    return render(
        request,
        "App_Allocation/Search_and_Select.html",
        context,
    )


# ########################  Allocate to PBS ##########################
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from App_Allocation.models import Temporary_Allocation, Final_Allocation, PBS, Item, Allocation_Number
from App_Allocation.forms import TemporaryAllocationForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation




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
            quantity = Decimal(quantity)   # convert to Decimal
        except (TypeError, ValueError, InvalidOperation):
            messages.error(request, "Invalid quantity entered.")
            return redirect("App_Allocation:allocate_item", allocation_id=allocation_id, item_id=item.id)

        existing_allocations = Temporary_Allocation.objects.filter(
            allocation_no=allocation_no_obj, item_primary_key=item.id
        )
        total_allocated = sum(existing.quantity for existing in existing_allocations)

        # # Check stock limits
        # print("####################################################################")
        # print("Quantity to allocate:", quantity)
        # print("Total already allocated:", total_allocated)
        # print("Item stock available:", item.quantity_of_item)
        # print(quantity ,">", item.quantity_of_item, "=", quantity > item.quantity_of_item)
        # print("####################################################################")


        # if quantity + total_allocated > item.quantity_of_item:
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
            allocation.quantity = quantity  # make sure form field aligns

            # Save only if stock is enough
            if item.quantity_of_item >= quantity:
                allocation.save()
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
