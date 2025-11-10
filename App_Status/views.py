# App_Status\views.py
from django.shortcuts import render
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime

def status_page(request):
    """Renders the package and item entry page with dynamic search functionality"""
    
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
                    combined_q &= Q(package__packageId__icontains=query)
                elif filter_by == "Item Name":
                    combined_q &= Q(name__icontains=query)
                elif filter_by == "Warehouse":
                    combined_q &= Q(warehouse__icontains=query)
                elif filter_by == "Unit":
                    combined_q &= Q(unit_of_item__icontains=query)
                elif filter_by == "Entry/Update date":
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

    context = {
        "items": all_items,
    }
    context.update(active_filters) # Add active filters back to context for template

    return render(
        request,
        "App_Status/status.html",
        context,
    )
