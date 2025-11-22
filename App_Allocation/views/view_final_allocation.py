# App_Allocation\views\view_final_allocation.py

#####################################################################
### VVI: This now shows Temporay_Allocation, not Final_Allocation ###
#####################################################################

from django.shortcuts import render
from App_Allocation.models import Temporary_Allocation
from django.db.models import Q

def final_allocation_search(request):
    query = request.GET.get("query", "")
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    results = Temporary_Allocation.objects.all().order_by('-created_at')

    if query:
        if filter_by == "All":
            # search across all relevant fields with exact (case-insensitive) match
            results = results.filter(
                Q(allocation_no__allocation_no__iexact=query)
                | Q(pbs__name__iexact=query)
                | Q(package__packageId__iexact=query)
                | Q(item__name__iexact=query)
                | Q(warehouse__iexact=query)
            )
        elif filter_by == "allocation_no":
            results = results.filter(allocation_no__allocation_no__iexact=query)
        elif filter_by == "pbs":
            results = results.filter(pbs__name__iexact=query)
        elif filter_by == "package":
            results = results.filter(package__packageId__iexact=query)
        elif filter_by == "item":
            results = results.filter(item__name__iexact=query)
        elif filter_by == "warehouse":
            results = results.filter(warehouse__iexact=query)

    if date_filter:
        results = results.filter(created_at__date=date_filter)

    context = {
        "items": results,
        "query": query,
        "filter_by": filter_by,
        "date_filter": date_filter,
    }

    return render(request, "App_Allocation/view_print_Final_Allocation.html", context)
