# App_Allocation\views\View_and_Confirm_Allocation_view.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Project_App_Allocation.models import Temporary_Allocation, Final_Allocation, Allocation_Number
from Project_App_Entry.models import Project_Item as Item
from Project_App_History.models import Project_History as History
import uuid

def view_confirm_allocation(request, allocation_id):
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    allocations = Temporary_Allocation.objects.filter(allocation_no=allocation_no_obj)

    return render(
        request,
        "Project_Templates/Project_App_Allocation/view_and_confirm_allocation.html",
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
        return redirect("Project_App_Allocation:view_confirm_allocation", allocation_id=allocation_id)

    return redirect("Project_App_Allocation:allocate_item", allocation_id=allocation_no_obj)



from django.utils import timezone

@login_required
def confirm_allocation(request, allocation_id):
    # Get the Allocation_Number object by ID
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)

    # Filter Temporary_Allocation entries with matching allocation_no (as integer)
    allocations = Temporary_Allocation.objects.filter(allocation_no=allocation_no_obj.id)

    if request.method == "POST":
        for allocation in allocations:

            unique_id_for_History = uuid.uuid4()

            dhaka_time = timezone.localtime(timezone.now())
            # Create Final_Allocation entry
            Final_Allocation.objects.create(
                allocation_no=allocation.allocation_no,
                item_primary_key=allocation.item_primary_key,
                pbs=allocation.pbs,
                project=allocation.project,
                item=allocation.item,
                warehouse=allocation.warehouse,
                quantity=allocation.quantity,
                # price=allocation.price,
                unit_of_item=allocation.unit_of_item,
                status  = "Allocated",
                history_GUID = unique_id_for_History
            )

            # Update Allocation_Number status to "Allocated"
            allocation_no_obj.status = "Allocated"
            allocation_no_obj.save()

            # Create History entry
            History.objects.create(
                GUID = unique_id_for_History,
                allocation_no=allocation.allocation_no.allocation_no, 
                pbs=allocation.pbs,
                project=allocation.project.projectId,
                item=allocation.item,
                unit_of_item=allocation.unit_of_item,
                warehouse=allocation.warehouse,
                quantity=allocation.quantity,
                # price=allocation.price,
                created_at=dhaka_time,  
                status="Allocated",
                remarks="Allocated at: <b>" + dhaka_time.strftime("%Y-%m-%d %I:%M %p") + "</b>",
            )

        # Delete temporary allocations
        allocations.delete()

        # Show success message and redirect
        messages.success(request, "Allocation confirmed successfully.")
        return redirect("Project_App_Allocation:select_allocation_number")

    # If not POST, redirect to allocation item page
    return redirect("Project_App_Allocation:allocate_item", allocation_id=allocation_id)


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
        return redirect("Project_App_Allocation:view_confirm_allocation", allocation_id=allocation.allocation_no.id)

    return redirect("Project_App_Allocation:view_confirm_allocation", allocation_id=allocation.allocation_no.id)