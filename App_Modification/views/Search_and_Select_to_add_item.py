from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from App_Allocation.models import Allocation_Number, Final_Allocation
from django.contrib import messages


@login_required
def Search_and_Select_Items(request, allocation_id=None):
    """Allows searching and selecting a new item to add to a given allocation."""
    query = request.GET.get("query", "").strip()
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    items = Item.objects.all()

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

    if filter_by == "Entry/Update date" and date_filter:
        try:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            items = items.filter(created_at__date=date_obj.date())
        except ValueError:
            pass

    items = items.order_by("package__packageId")

    allocation_number = None
    if allocation_id:
        try:
            allocation = Allocation_Number.objects.get(id=allocation_id)
            allocation_number = allocation.allocation_no
        except Allocation_Number.DoesNotExist:
            messages.error(request, "Invalid Allocation Number.")

    return render(
        request,
        "App_Modification/Search_and_Select_Items.html",
        {
            "items": items,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
            "allocation_number": allocation_number,
            "allocation_id": allocation_id,
        },
    )
