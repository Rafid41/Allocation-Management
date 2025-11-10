from django.shortcuts import render
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime

def status_page(request):
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

    # Order the results by Item Name
    items = items.order_by("name")

    return render(
        request,
        "App_Status/status.html",
        {
            "items": items,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
        },
    )
