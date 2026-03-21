from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.core.paginator import Paginator
from ..models import PBS_List, Zonals_Balance

def zonal_sum_view(request, pbs_id):
    """
    Groups all Zonal Balance records for a given PBS by item name and unit,
    summing up all storage/category columns.
    """
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    search_query = request.GET.get('search', '').strip()
    
    # Filter by PBS
    balances = Zonals_Balance.objects.filter(pbs=pbs)
    
    if search_query:
        balances = balances.filter(item__item_name__icontains=search_query)
        
    # Group by item and unit, sum all categories
    # item__item_name and item__unit are the grouping keys
    summary = balances.values('item__item_name', 'item__unit').annotate(
        total_deposit_work=Sum('deposit_work'),
        total_mcep_dmd=Sum('mcep_dmd'),
        total_mcep_kd=Sum('mcep_kd'),
        total_mcep_bd=Sum('mcep_bd'),
        total_other=Sum('other'),
        total_om_store=Sum('om_store'),
        total_own_stock=Sum('own_stock')
    ).order_by('item__item_name')
    
    # Re-wrap the values list into a list of simplified objects/dicts for easier template handling
    # and calculate the row-wise total.
    processed_summary = []
    for entry in summary:
        row_total = (
            (entry['total_deposit_work'] or 0) +
            (entry['total_mcep_dmd'] or 0) +
            (entry['total_mcep_kd'] or 0) +
            (entry['total_mcep_bd'] or 0) +
            (entry['total_other'] or 0) +
            (entry['total_om_store'] or 0) +
            (entry['total_own_stock'] or 0)
        )
        processed_summary.append({
            'item_name': entry['item__item_name'],
            'unit': entry['item__unit'],
            'deposit_work': entry['total_deposit_work'] or 0,
            'mcep_dmd': entry['total_mcep_dmd'] or 0,
            'mcep_kd': entry['total_mcep_kd'] or 0,
            'mcep_bd': entry['total_mcep_bd'] or 0,
            'other': entry['total_other'] or 0,
            'om_store': entry['total_om_store'] or 0,
            'own_stock': entry['total_own_stock'] or 0,
            'total': row_total
        })

    paginator = Paginator(processed_summary, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    print_view = request.GET.get('print_view') == 'true'

    context = {
        'pbs': pbs,
        'summary': page_obj,
        'search_query': search_query,
        'is_print_view': print_view,
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/zonal_sum.html", context)
