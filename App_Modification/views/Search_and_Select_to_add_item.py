from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from App_Allocation.models import Allocation_Number, Final_Allocation
from django.contrib import messages


@login_required
def Search_and_Select_Items(request, allocation_id=None):
    """Allows searching and selecting a new item to add to a given allocation."""
    # Filter Logic
    items = Item.objects.all()
    applied_filters = []
    
    # Iterate through potential filters (supporting multiple rows)
    for i in range(1, 10):
        filter_type = request.GET.get(f"filter_type_{i}")
        filter_value = request.GET.get(f"filter_value_{i}")

        if filter_value:
             filter_value = filter_value.strip()

        if not filter_type or filter_type == "no_condition" or not filter_value:
            continue
        
        applied_filters.append({
            "type": filter_type,
            "value": filter_value
        })

        if filter_type == "package":
            items = items.filter(package__packageId__iexact=filter_value)
        elif filter_type == "item":
            items = items.filter(name__iexact=filter_value)
        elif filter_type == "warehouse":
            items = items.filter(warehouse__iexact=filter_value)
    
    items = items.order_by("package__packageId")

    allocation_number = None
    if allocation_id:
        try:
            allocation = Allocation_Number.objects.get(id=allocation_id)
            allocation_number = allocation.allocation_no
        except Allocation_Number.DoesNotExist:
            messages.error(request, "Invalid Allocation Number.")

    # Get distinct warehouses for dropdown
    warehouses = list(Item.objects.values_list('warehouse', flat=True).distinct())

    return render(
        request,
        "App_Modification/Search_and_Select_Items.html",
        {
            "items": items,
            "allocation_number": allocation_number,
            "allocation_id": allocation_id,
            "warehouse_json": json.dumps(warehouses),
        },
    )
