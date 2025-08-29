from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from App_Allocation.models import Final_Allocation, Allocation_Number
from App_Entry.models import Item
from App_History.models import History

@login_required
def view_final_allocation(request, allocation_id):
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    allocations = Final_Allocation.objects.filter(allocation_no=allocation_no_obj)

    return render(
        request,
        "App_Modification/view_and_delete_Item.html",
        {
            "allocations": allocations,
            "allocation_no_obj": allocation_no_obj,
        },
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from App_Allocation.models import Final_Allocation, Item, Allocation_Number  # Ensure all are imported

@login_required
def delete_final_allocation_entry(request, allocation_id):
    allocation = get_object_or_404(Final_Allocation, id=allocation_id)
    item = get_object_or_404(Item, id=allocation.item_primary_key)
    allocation_no_obj = allocation.allocation_no
    allocation_no_id = allocation_no_obj.id  # For redirect
    allocation_no_str = allocation_no_obj.allocation_no  # For History

    if request.method == "POST":
        dhaka_time = timezone.localtime(timezone.now())
        remarks_text = "Deleted at: <b>" + dhaka_time.strftime("%Y-%m-%d %I:%M %p")+"</b>"


        #  If this allocation has a GUID, check for previous History entry
        if allocation.history_GUID:
            old_history = History.objects.filter(
                GUID=allocation.history_GUID,
                status="Allocated"
            ).first()
            if old_history:
                old_history.delete()  #  remove the original allocated history


        # ✅ Log only the deleted item to History
        History.objects.create(
            allocation_no=allocation_no_str,
            pbs=allocation.pbs.name,
            package=allocation.package.packageId,
            item=allocation.item.name,
            unit_of_item=allocation.unit_of_item,
            warehouse=allocation.warehouse,
            quantity=allocation.quantity,
            price=allocation.price,
            created_at=dhaka_time,
            status="Modified",
            remarks=remarks_text,
            remarks_status="Deleted"
        )

        # ✅ Restore deleted item's quantity
        item.quantity_of_item += allocation.quantity
        item.save()

        # ✅ Delete the selected Final_Allocation entry
        allocation.delete()

        # ✅ Update Allocation_Number status to "Modified"
        allocation_no_obj.status = "Modified"
        allocation_no_obj.save()

        messages.success(request, "Allocation entry deleted successfully.")
        return redirect("App_Modification:view_final_allocation", allocation_id=allocation_no_id)

    return redirect("App_Modification:view_final_allocation", allocation_id=allocation_no_id)
