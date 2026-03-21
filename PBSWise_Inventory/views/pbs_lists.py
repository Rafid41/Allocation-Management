from django.shortcuts import render
# Reusing the PBS_List from PBSWise_Balance as it contains the canonical list of regions
from PBSWise_Balance.models import PBS_List

def pbs_list_view(request):
    """View to list all PBS items for Inventory Management (Read-only)."""
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        pbs_items = PBS_List.objects.filter(pbs_name__icontains=search_query).order_by('pbs_name')
    else:
        pbs_items = PBS_List.objects.all().order_by('pbs_name')
    
    # We pass 'can_modify' as False to ensure the template hides all Add/Edit/Delete UI
    context = {
        'pbs_items': pbs_items,
        'search_query': search_query,
        'can_modify': False, 
    }
    return render(request, "PBSWise_Templates/PBSWise_Inventory/pbs_lists.html", context)
