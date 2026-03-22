from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from io import BytesIO
from PBSWise_Balance.models import PBS_List, Zonal_Items, Zonals_Balance
from App_Admin_Panel.models import PaginationManager

@login_required
def pbswise_summary_view(request):
    """
    Authorized view for a high-fidelity summary of PBS assets.
    Aggregates inventory data across all regional project portals.
    """
    allowed_groups = ["Editor", "View History and Status only"]
    if not request.user.is_superuser and request.user.user_group.user_group_type not in allowed_groups:
        return redirect("App_User_Group:access-denied")

    # Initial Data Acquisition
    search_item = request.GET.get('item_name', '').strip()
    is_print_view = request.GET.get('print_view') == 'true'

    # Filter Items
    item_queryset = Zonal_Items.objects.all().order_by('item_name')
    if search_item:
        item_queryset = item_queryset.filter(item_name__icontains=search_item)

    # Fetch all PBS units for column generation
    pbs_list = PBS_List.objects.all().order_by('pbs_name')

    # Pagination Controller
    if is_print_view:
        items_on_page = item_queryset
    else:
        try:
            limit = PaginationManager.load().table_pagination_limit
        except:
            limit = 50
        
        paginator = Paginator(item_queryset, limit)
        page_number = request.GET.get('page', 1)
        try:
            items_on_page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            items_on_page = paginator.page(1)

    # Aggregate Data - We build a matrix of (Item, PBS) -> Total
    # Optimized query: get all balances for the items on current page
    item_ids = [it.id for it in items_on_page]
    balances = Zonals_Balance.objects.filter(item_id__in=item_ids).values('item_id', 'pbs_id').annotate(item_sum=Sum('total'))
    
    # Map for easy lookup: data_map[item_id][pbs_id] = sum
    data_map = {}
    for b in balances:
        i_id = b['item_id']
        p_id = b['pbs_id']
        if i_id not in data_map: data_map[i_id] = {}
        data_map[i_id][str(p_id)] = b['item_sum']

    # Final Data List for Template
    summary_data = []
    for item in items_on_page:
        row = {
            'item': item,
            'unit': item.unit,
            'pbs_values': [],
            'row_total': 0.0
        }
        for pbs in pbs_list:
            val = data_map.get(item.id, {}).get(str(pbs.id), 0.0)
            row['pbs_values'].append(val)
            row['row_total'] += val
        summary_data.append(row)

    context = {
        'items': items_on_page,
        'summary_data': summary_data,
        'pbs_list': pbs_list,
        'item_name': search_item,
        'is_print_view': is_print_view,
    }
    return render(request, "PBSWise_Templates/PBSWise_Summary/PBSWise_Summary.html", context)

def get_summary_suggestions_ajax(request):
    """AJAX help for absolute unique item suggestions in summary reporting."""
    query = request.GET.get('query', '')
    suggestions = Zonal_Items.objects.filter(item_name__icontains=query).values_list('item_name', flat=True).distinct()[:10]
    return JsonResponse({'suggestions': list(suggestions)})
