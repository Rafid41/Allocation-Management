'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from App_Allocation.models import Temporary_Allocation, Final_Allocation, Allocation_Number, Item

def confirm_allocation_view(request):
    query = request.GET.get("query", "")
    allocations = []

    if query:
        allocations = Temporary_Allocation.objects.filter(allocation_no__allocation_no=query)

    return render(
        request,
        "App_Allocation\confirm_allocation.html",
        {"allocations": allocations, "query": query},
    )


def delete_allocation(request, allocation_no):
    try:
        allocation = get_object_or_404(Allocation_Number, allocation_no=allocation_no)
        allocation.delete()
        messages.success(request, f"Allocation {allocation_no} deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting allocation: {str(e)}")

    return redirect("App_Allocation:confirm_allocation")


def confirm_allocation(request, allocation_no):
    allocations = Temporary_Allocation.objects.filter(allocation_no__allocation_no=allocation_no)

    if not allocations.exists():
        messages.error(request, "No allocations found.")
        return redirect("App_Allocation:confirm_allocation")

    item_quantities = {}

    for allocation in allocations:
        if allocation.item_primary_key in item_quantities:
            item_quantities[allocation.item_primary_key] += allocation.quantity
        else:
            item_quantities[allocation.item_primary_key] = allocation.quantity

    for item_pk, total_quantity in item_quantities.items():
        item = get_object_or_404(Item, pk=item_pk)

        if total_quantity > item.quantity_of_item:
            messages.error(request, f"{item.name} exceeds available limit.")
            return redirect("App_Allocation:confirm_allocation")

    for allocation in allocations:
        item = get_object_or_404(Item, pk=allocation.item_primary_key)
        item.quantity_of_item -= allocation.quantity
        item.save()

        Final_Allocation.objects.create(
            allocation_no=allocation.allocation_no,
            item_primary_key=allocation.item_primary_key,
            pbs=allocation.pbs,
            package=allocation.package,
            item=allocation.item,
            warehouse=allocation.warehouse,
            quantity=allocation.quantity,
            price=allocation.price,
        )

    allocations.delete()
    messages.success(request, "Allocation confirmed successfully.")
    return redirect("App_Allocation:confirm_allocation")
'''

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from App_Allocation.models import Temporary_Allocation, Final_Allocation, Allocation_Number
from App_Entry.models import Item

def view_confirm_allocation(request, allocation_id):
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    allocations = Temporary_Allocation.objects.filter(allocation_no=allocation_no_obj)

    return render(
        request,
        "App_Allocation/view_and_confirm_allocation.html",
        {
            "allocations": allocations,
            "allocation_no_obj": allocation_no_obj,
        },
    )


@login_required
def delete_all_allocations(request, allocation_id):
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    allocations = Temporary_Allocation.objects.filter(allocation_no=allocation_no_obj)

    if request.method == "POST":
        for allocation in allocations:
            item = get_object_or_404(Item, id=allocation.item_primary_key)
            item.quantity_of_item += allocation.quantity
            item.save()
            allocation.delete()
        
        messages.success(request, "All allocations deleted successfully.")
        return redirect("App_Allocation:view_confirm_allocation", allocation_id=allocation_id)

    return redirect("App_Allocation:allocate_item", allocation_id=allocation_no_obj)

@login_required
def confirm_allocation(request, allocation_id):
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    allocations = Temporary_Allocation.objects.filter(allocation_no=allocation_no_obj)

    if request.method == "POST":
        for allocation in allocations:
            Final_Allocation.objects.create(
                allocation_no=allocation.allocation_no,
                item_primary_key=allocation.item_primary_key,
                pbs=allocation.pbs,
                package=allocation.package,
                item=allocation.item,
                warehouse=allocation.warehouse,
                quantity=allocation.quantity,
                price=allocation.price
            )
        
        allocations.delete()
        messages.success(request, "Allocation confirmed successfully.")
        return redirect("App_Allocation:Search_and_Select", allocation_id=allocation_id)

    return redirect("App_Allocation:allocate_item", allocation_id=allocation_id)


@login_required
def delete_allocation_in_view_page(request, allocation_id):
    allocation = get_object_or_404(Temporary_Allocation, id=allocation_id)
    item = get_object_or_404(Item, id=allocation.item_primary_key)

    if request.method == "POST":
        # Add back the allocated quantity to the Item stock
        item.quantity_of_item += allocation.quantity
        item.save()
        
        # Delete the allocation entry
        allocation.delete()
        
        messages.success(request, "Allocation entry deleted successfully.")
        return redirect("App_Allocation:view_confirm_allocation", allocation_id=allocation.allocation_no.id)

    return redirect("App_Allocation:view_confirm_allocation", allocation_id=allocation.allocation_no.id)