# App_Allocation\views\view_final_allocation.py

#####################################################################
### VVI: This now shows Temporay_Allocation, not Final_Allocation ###
#####################################################################

from django.shortcuts import render
from App_Allocation.models import Temporary_Allocation
from django.db.models import Q

def final_allocation_search(request):
    results = Temporary_Allocation.objects.all().order_by('-created_at')

    # Fetch unique warehouses for the dropdown
    unique_warehouses = sorted(list(set(
        Temporary_Allocation.objects.values_list('warehouse', flat=True).distinct()
    )))

    # Apply Dynamic Filters
    for i in range(1, 10):  # Supports up to 9 filters
        filter_type = request.GET.get(f"filter_type_{i}")
        filter_value = request.GET.get(f"filter_value_{i}")
        
        if filter_value:
            filter_value = filter_value.strip()

        # Skip empty or no-condition filters
        if not filter_type or filter_type == "no_condition" or not filter_value:
            continue
        
        # Apply filters based on type
        if filter_type == "allocation_no":
            results = results.filter(allocation_no__allocation_no__iexact=filter_value)
        elif filter_type == "pbs":
            results = results.filter(pbs__name__iexact=filter_value)
        elif filter_type == "package":
            results = results.filter(package__packageId__iexact=filter_value)
        elif filter_type == "item":
            results = results.filter(item__name__iexact=filter_value)
        elif filter_type == "warehouse":
            results = results.filter(warehouse__iexact=filter_value)

    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        
    print_view = request.GET.get("print_view") == "true"
    
    if print_view:
        items = results
    else:
        # Fetch dynamic pagination limit
        from App_Admin_Panel.models import PaginationManager
        try:
            limit = PaginationManager.load().table_pagination_limit
        except:
            limit = 50 # Fallback

        page = request.GET.get('page', 1)
        paginator = Paginator(results, limit)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

    context = {
        "items": items,
        "unique_warehouses": unique_warehouses,
        "is_print_view": print_view,
    }

    return render(request, "App_Allocation/view_print_Final_Allocation.html", context)
