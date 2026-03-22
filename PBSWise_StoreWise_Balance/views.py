from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from PBSWise_Balance.models import PBS_List, Zonal_Items, Zonals_Balance
from App_Admin_Panel.models import PaginationManager

@login_required
def storewise_balance_home_view(request):
    """
    Authorized home view for regional Storewise Balance analysis.
    """
    if not request.user.is_superuser and getattr(request.user.user_group, 'user_group_type', '') != "Editor":
        return redirect("App_User_Group:access-denied")

    return render(request, "PBSWise_Templates/PBSWise_StoreWise_Balance/storewise_balance_home.html")

@login_required
def store_detail_summary_view(request, store_slug):
    """
    Dynamic summary registry for specific regional store categories. 
    Aggregates absolute inventory levels across all 80+ PBS portals.
    """
    if not request.user.is_superuser and getattr(request.user.user_group, 'user_group_type', '') != "Editor":
        return redirect("App_User_Group:access-denied")

    # Store Mapping Suite
    store_map = {
        'om': {'field': 'om_store', 'label': 'O&M'},
        'own-stock': {'field': 'own_stock', 'label': 'OWN STOCK'},
        'deposit': {'field': 'deposit_work', 'label': 'DEPOSIT WORK'},
        'mcep-dmd': {'field': 'mcep_dmd', 'label': 'MCEP DMD'},
        'mcep-kd': {'field': 'mcep_kd', 'label': 'MCEP KD'},
        'mcep-bd': {'field': 'mcep_bd', 'label': 'MCEP BD'},
        'other': {'field': 'other', 'label': 'OTHER'},
        'all-projects': {'field': 'all_projects', 'label': 'ALL PROJECTS'},
    }

    if store_slug not in store_map:
        return redirect("PBSWise_StoreWise_Balance:storewise_balance_home")

    store_info = store_map[store_slug]
    
    # Filter and Pagination Parameters
    search_item = request.GET.get('item_name', '').strip()
    is_print_view = request.GET.get('print_view') == 'true'

    item_queryset = Zonal_Items.objects.all().order_by('item_name')
    if search_item:
        item_queryset = item_queryset.filter(item_name__icontains=search_item)

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

    # Absolute Data Aggregation Engine
    item_ids = [it.id for it in items_on_page]
    balances_query = Zonals_Balance.objects.filter(item_id__in=item_ids).values('item_id', 'pbs_id')
    
    # Dynamic field selection for the selected store
    if store_slug == 'all-projects':
        balances = balances_query.annotate(
            item_sum=Sum(F('mcep_dmd') + F('mcep_kd') + F('mcep_bd') + F('other'))
        )
    else:
        balances = balances_query.annotate(item_sum=Sum(store_info['field']))
    
    # Map for easy matrix lookup: data_map[item_id][pbs_id] = sum
    data_map = {}
    for b in balances:
        i_id = b['item_id']
        p_id = str(b['pbs_id'])
        if i_id not in data_map: data_map[i_id] = {}
        data_map[i_id][p_id] = b['item_sum']

    # Matrix Construction Suite
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
        'store_label': store_info['label'],
        'store_slug': store_slug,
        'item_name': search_item,
        'is_print_view': is_print_view,
    }
    return render(request, "PBSWise_Templates/PBSWise_StoreWise_Balance/store_detail_summary.html", context)
