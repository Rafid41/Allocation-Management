# App_Allocation\views\view_final_allocation.py
from django.shortcuts import render
from App_Allocation.models import Final_Allocation

def history(request):
    query = request.GET.get("query", "")
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    results = Final_Allocation.objects.all().order_by('-created_at')

    if query:
        if filter_by == "allocation_no":
            results = results.filter(allocation_no__allocation_no__icontains=query)
        elif filter_by == "pbs":
            results = results.filter(pbs__pbs_name__icontains=query)
        elif filter_by == "package":
            results = results.filter(package__packageId__icontains=query)
        elif filter_by == "item":
            results = results.filter(item__name__icontains=query)
        elif filter_by == "warehouse":
            results = results.filter(warehouse__icontains=query)

    if date_filter:
        results = results.filter(created_at__date=date_filter)

    context = {
        "items": results,
        "query": query,
        "filter_by": filter_by,
        "date_filter": date_filter,
    }

    return render(request, "App_History/view_and_print_history.html", context)
