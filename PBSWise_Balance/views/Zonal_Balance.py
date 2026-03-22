from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .all_pbs_list_page import check_editor_permission
from ..models import PBS_List, PBS_Zonals, Zonal_Items, Zonals_Balance
from App_Admin_Panel.models import PaginationManager
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from App_Entry.models import Item as MainItem

def zonal_balance_view(request):
    """View to list and search Zonal Balances."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")

    # Initial queryset
    queryset = Zonals_Balance.objects.all().select_related('pbs', 'zonal', 'item')

    # Sorting: 1st PBS, 2nd Zonal
    queryset = queryset.order_by('pbs__pbs_name', 'zonal__zonal_name', 'item__item_name')

    # Search Logic (Exact but case insensitive as per history page style)
    pbs_id = request.GET.get('pbs_id', '').strip()
    zonal_id = request.GET.get('zonal_id', '').strip()
    item_id = request.GET.get('item_id', '').strip()

    if pbs_id:
        queryset = queryset.filter(pbs_id=pbs_id)
    if zonal_id:
        queryset = queryset.filter(zonal_id=zonal_id)
    if item_id:
        queryset = queryset.filter(item_id=item_id)

    # Print view logic (Bypass pagination)
    print_view = request.GET.get('print_view') == 'true'
    
    if print_view:
        items = queryset
    else:
        # Fetch dynamic pagination limit
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

    # Dropdowns for search and add/edit
    pbs_all = PBS_List.objects.all().order_by('pbs_name')
    items_all = Zonal_Items.objects.all().order_by('item_name')
    units = [choice for choice in MainItem.UNIT_CHOICES]

    context = {
        'items': items,
        'pbs_all': pbs_all,
        'items_all': items_all,
        'units': units,
        'can_modify': True,
        'selected_pbs': pbs_id,
        'selected_zonal': zonal_id,
        'selected_item': item_id,
        'is_print_view': print_view,
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/Zonal_Balance.html", context)

def zonal_balance_add(request):
    """Handle adding a Zonal Balance record."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")

    if request.method == "POST":
        pbs_id = request.POST.get('pbs')
        zonal_id = request.POST.get('zonal')
        item_id = request.POST.get('item')
        
        # Unique check
        if Zonals_Balance.objects.filter(pbs_id=pbs_id, zonal_id=zonal_id, item_id=item_id).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'duplicate'})
            messages.error(request, "A record with this PBS, Zonal and Item already exists.")
            return redirect("PBSWise_Balance:zonal_balance_view")

        try:
            record = Zonals_Balance(
                pbs_id=pbs_id,
                zonal_id=zonal_id,
                item_id=item_id,
                description=request.POST.get('description', '').strip(),
                deposit_work=float(request.POST.get('deposit_work', 0) or 0),
                mcep_dmd=float(request.POST.get('mcep_dmd', 0) or 0),
                mcep_kd=float(request.POST.get('mcep_kd', 0) or 0),
                mcep_bd=float(request.POST.get('mcep_bd', 0) or 0),
                other=float(request.POST.get('other', 0) or 0),
                om_store=float(request.POST.get('om_store', 0) or 0),
                own_stock=float(request.POST.get('own_stock', 0) or 0),
            )
            record.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Balance entry added successfully.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f"Error adding record: {str(e)}")

    return redirect("PBSWise_Balance:zonal_balance_view")

def zonal_balance_edit(request, record_id):
    """Handle editing a Zonal Balance record."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")

    record = get_object_or_404(Zonals_Balance, id=record_id)
    if request.method == "POST":
        pbs_id = request.POST.get('pbs')
        zonal_id = request.POST.get('zonal')
        item_id = request.POST.get('item')

        # Unique check (excluding current record)
        if Zonals_Balance.objects.filter(pbs_id=pbs_id, zonal_id=zonal_id, item_id=item_id).exclude(id=record_id).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'duplicate'})
            messages.error(request, "A record with this PBS, Zonal and Item already exists.")
            return redirect("PBSWise_Balance:zonal_balance_view")

        try:
            record.pbs_id = pbs_id
            record.zonal_id = zonal_id
            record.item_id = item_id
            record.description = request.POST.get('description', '').strip()
            record.deposit_work = float(request.POST.get('deposit_work', 0) or 0)
            record.mcep_dmd = float(request.POST.get('mcep_dmd', 0) or 0)
            record.mcep_kd = float(request.POST.get('mcep_kd', 0) or 0)
            record.mcep_bd = float(request.POST.get('mcep_bd', 0) or 0)
            record.other = float(request.POST.get('other', 0) or 0)
            record.om_store = float(request.POST.get('om_store', 0) or 0)
            record.own_stock = float(request.POST.get('own_stock', 0) or 0)
            record.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Balance entry updated successfully.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f"Error updating record: {str(e)}")

    return redirect("PBSWise_Balance:zonal_balance_view")

def zonal_balance_delete(request, record_id):
    """Handle deleting a Zonal Balance record."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")

    record = get_object_or_404(Zonals_Balance, id=record_id)
    record.delete()
    messages.success(request, "Balance entry deleted successfully.")
    return redirect("PBSWise_Balance:zonal_balance_view")

# AJAX HELPERS
def get_zonals_by_pbs(request):
    """Helper to fetch zonals for a PBS (AJAX)."""
    pbs_id = request.GET.get('pbs_id')
    if not pbs_id:
        return JsonResponse({'zonals': []})
    
    zonals = PBS_Zonals.objects.filter(pbs_id=pbs_id).order_by('zonal_name').values('id', 'zonal_name')
    return JsonResponse({'zonals': list(zonals)})

def check_unique_zonal_balance(request):
    """Helper to check record uniqueness live (AJAX)."""
    pbs_id = request.GET.get('pbs_id')
    zonal_id = request.GET.get('zonal_id')
    item_id = request.GET.get('item_id')
    exclude_id = request.GET.get('exclude_id')

    if not (pbs_id and zonal_id and item_id):
        return JsonResponse({'exists': False})

    query = Zonals_Balance.objects.filter(pbs_id=pbs_id, zonal_id=zonal_id, item_id=item_id)
    if exclude_id:
        query = query.exclude(id=exclude_id)
    
    return JsonResponse({'exists': query.exists()})
