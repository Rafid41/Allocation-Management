from django.shortcuts import render
from App_Allocation.models import Final_Allocation

def generate_report(request):
    query = request.GET.get("query", "").strip()
    allocations = Final_Allocation.objects.all().order_by('-created_at')

    if query:
        allocations = allocations.filter(allocation_no__allocation_no__icontains=query)

    context = {
        "allocations": allocations,
        "query": query,
    }

    return render(request, "App_Allocation/generate_and_print_report.html", context)
