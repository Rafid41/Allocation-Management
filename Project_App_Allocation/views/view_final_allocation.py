# App_Allocation\views\view_final_allocation.py
from django.shortcuts import render
from Project_App_Allocation.models import Final_Allocation

def final_allocation_search(request):
    query = request.GET.get("query", "")
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    results = Final_Allocation.objects.all().order_by('-created_at')

    if query:
        if filter_by == "allocation_no":
            results = results.filter(allocation_no__allocation_no__icontains=query)
        elif filter_by == "pbs":
            results = results.filter(pbs__name__icontains=query)
        elif filter_by == "project":
            results = results.filter(project__projectId__icontains=query)
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

    return render(request, "Project_Templates/Project_App_Allocation/view_print_Final_Allocation.html", context)
