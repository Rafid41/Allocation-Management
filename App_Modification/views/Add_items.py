from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from App_Allocation.models import Final_Allocation, PBS, Item, Allocation_Number
from App_Modification.forms import FinalAllocationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from App_History.models import History


@login_required
def add_item(request, allocation_id, item_id):
    item = get_object_or_404(Item, id=item_id)
    allocation_no_obj = get_object_or_404(Allocation_Number, id=allocation_id)
    pbss = PBS.objects.all()

    if request.method == "POST":
        form = FinalAllocationForm(request.POST)
        pbs_id = request.POST.get("pbs")
        quantity = request.POST.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity entered.")
            return redirect("App_Modification:add_item", allocation_id=allocation_id, item_id=item.id)

        existing_allocations = Final_Allocation.objects.filter(
            allocation_no=allocation_no_obj, item_primary_key=item.id
        )
        total_allocated = sum(existing.quantity for existing in existing_allocations)

        if total_allocated + quantity > item.quantity_of_item:
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
            allocation.quantity = quantity

            if item.quantity_of_item >= quantity:
                allocation.save()
                item.quantity_of_item -= quantity
                item.save()

                # ✅ Log to History
                dhaka_time = timezone.localtime(timezone.now())
                remarks_text = "Added Item at: <b>" + dhaka_time.strftime("%Y-%m-%d %I:%M %p") + "</b>"

                History.objects.create(
                    allocation_no=allocation_no_obj.allocation_no,
                    pbs=allocation.pbs.name,
                    package=allocation.package.packageId,
                    item=allocation.item.name,
                    warehouse=allocation.warehouse,
                    quantity=allocation.quantity,
                    price=allocation.price,
                    created_at=dhaka_time,
                    status="Modified",
                    remarks=remarks_text,
                )

                # ✅ Update Allocation_Number status to "Modified"
                allocation_no_obj.status = "Modified"
                allocation_no_obj.save()

                messages.success(request, "Item allocated and logged successfully!")

                # ✅ Redirect to search and select page
                return redirect("App_Modification:search_and_select_item", allocation_id=allocation_id)
            else:
                messages.error(request, "Not enough stock available for allocation.")

            return redirect("App_Modification:add_item", allocation_id=allocation_id, item_id=item.id)

    else:
        form = FinalAllocationForm()

    allocations = Final_Allocation.objects.filter(allocation_no=allocation_no_obj).order_by("-created_at")

    return render(
        request,
        "App_Modification/add_item.html",
        {
            "form": form,
            "item": item,
            "allocation_no_obj": allocation_no_obj,
            "pbss": pbss,
            "allocations": allocations,
        },
    )
