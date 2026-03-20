from django.shortcuts import render, get_object_or_404
from ..models import PBS_Zonals, Zonals_Balance, Zonal_Items, PBS_List
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App_Admin_Panel.models import PaginationManager
from django.http import JsonResponse
from App_Entry.models import Item as MainItem

def zonal_details_view(request, zonal_id):
    zonal = get_object_or_404(PBS_Zonals, id=zonal_id)
    pbs = zonal.pbs
    
    # Initial queryset
    queryset = Zonals_Balance.objects.filter(pbs=pbs, zonal=zonal).select_related('item').order_by('item__item_name')
    
    # Search Logic (Only by Item Name as per instruction)
    item_id = request.GET.get('item_id', '').strip()
    if item_id:
        queryset = queryset.filter(item_id=item_id)
        
    # Print/Export bypass
    is_print_view = request.GET.get('print_view') == 'true'
    
    if is_print_view:
        items = queryset
    else:
        # Dynamic Pagination
        try:
            limit = PaginationManager.load().table_pagination_limit
        except:
            limit = 50

        page_number = request.GET.get('page', 1)
        paginator = Paginator(queryset, limit)
        
        try:
            items = paginator.page(page_number)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
            
    # Dropdowns for search
    items_all = Zonal_Items.objects.all().order_by('item_name')
    
    context = {
        'zonal': zonal,
        'pbs': pbs,
        'items': items,
        'selected_item': item_id,
        'items_all': items_all,
        'is_print_view': is_print_view,
    }
    
    return render(request, "PBSWise_Templates/PBSWise_Balance/zonal_details.html", context)
