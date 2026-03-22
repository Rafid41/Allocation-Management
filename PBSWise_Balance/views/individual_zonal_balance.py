from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .all_pbs_list_page import check_pbs_management_permission, get_pbs_username
from ..models import PBS_List, PBS_Zonals, Zonal_Items, Zonals_Balance
from App_Admin_Panel.models import PaginationManager
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App_Entry.models import Item as MainItem

def manage_balance_view(request, pbs_id):
    """View to list and search Zonal Balances for a specific regional PBS."""
    if not check_pbs_management_permission(request.user):
        messages.error(request, "Access Denied.")
        return redirect("App_Home:home_page")

    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    # Regional security check
    if request.user.user_group.user_group_type == "Specific_PBS_Account":
        if request.user.username != get_pbs_username(pbs.pbs_name):
            return redirect("App_User_Group:access-denied")

    # Initial queryset - strictly filtered by the current PBS
    queryset = Zonals_Balance.objects.filter(pbs=pbs).select_related('zonal', 'item')

    # Search Parameters (PBS is implicit)
    zonal_id = request.GET.get('zonal_id', '').strip()
    item_id = request.GET.get('item_id', '').strip()

    if zonal_id:
        queryset = queryset.filter(zonal_id=zonal_id)
    if item_id:
        queryset = queryset.filter(item_id=item_id)

    queryset = queryset.order_by('zonal__zonal_name', 'item__item_name')

    # Handle View logic (Print vs Pagination)
    print_view = request.GET.get('print_view') == 'true'
    if print_view:
        items = queryset
    else:
        try:
            limit = PaginationManager.load().table_pagination_limit
        except:
            limit = 50
        page_number = request.GET.get('page', 1)
        paginator = Paginator(queryset, limit)
        try:
            items = paginator.get_page(page_number)
        except:
            items = paginator.get_page(1)

    # Dropdowns for UI forms
    zonals_all = PBS_Zonals.objects.filter(pbs=pbs).order_by('zonal_name')
    items_all = Zonal_Items.objects.all().order_by('item_name')
    units = [choice for choice in MainItem.UNIT_CHOICES]

    context = {
        'pbs': pbs,
        'items': items,
        'zonals_all': zonals_all,
        'items_all': items_all,
        'units': units,
        'selected_zonal': zonal_id,
        'selected_item': item_id,
        'is_print_view': print_view,
        'can_modify': True,
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/manage_individual_zonal_balance.html", context)

def manage_balance_add(request, pbs_id):
    """Add a balance record pre-locked to a specific PBS."""
    if not check_pbs_management_permission(request.user):
        return redirect("App_User_Group:access-denied")

    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    # 🕵️ Security: For Specific_PBS_Account, only allow access to their own PBS
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.user_group.user_group_type == "Specific_PBS_Account":
            if request.user.username != get_pbs_username(pbs.pbs_name):
                return redirect("App_User_Group:access-denied")
    if request.method == "POST":
        zonal_id = request.POST.get('zonal')
        item_id = request.POST.get('item')
        
        # Uniqueness check
        if Zonals_Balance.objects.filter(pbs=pbs, zonal_id=zonal_id, item_id=item_id).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'duplicate'})
            messages.error(request, "Record Conflict: This Zonal and Item combination already exists for this PBS.")
            return redirect("PBSWise_Balance:manage_balance_view", pbs_id=pbs_id)

        try:
            # Prevent negative numbers
            deposit_work = float(request.POST.get('deposit_work', 0) or 0)
            mcep_dmd = float(request.POST.get('mcep_dmd', 0) or 0)
            mcep_kd = float(request.POST.get('mcep_kd', 0) or 0)
            mcep_bd = float(request.POST.get('mcep_bd', 0) or 0)
            other = float(request.POST.get('other', 0) or 0)
            om_store = float(request.POST.get('om_store', 0) or 0)
            own_stock = float(request.POST.get('own_stock', 0) or 0)

            if any(val < 0 for val in [deposit_work, mcep_dmd, mcep_kd, mcep_bd, other, om_store, own_stock]):
                raise ValueError("Negative values are not permitted for balance entries.")

            Zonals_Balance.objects.create(
                pbs=pbs,
                zonal_id=zonal_id,
                item_id=item_id,
                deposit_work=deposit_work,
                mcep_dmd=mcep_dmd,
                mcep_kd=mcep_kd,
                mcep_bd=mcep_bd,
                other=other,
                om_store=om_store,
                own_stock=own_stock,
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Store balance entry registered successfully.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f"Submission Error: {str(e)}")

    return redirect("PBSWise_Balance:manage_balance_view", pbs_id=pbs_id)

def manage_balance_edit(request, pbs_id, record_id):
    """Edit a balance record pre-locked to a specific PBS."""
    if not check_pbs_management_permission(request.user):
        return redirect("App_User_Group:access-denied")

    record = get_object_or_404(Zonals_Balance, id=record_id, pbs_id=pbs_id)
    pbs = record.pbs

    # 🕵️ Security: For Specific_PBS_Account, only allow access to their own PBS
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.user_group.user_group_type == "Specific_PBS_Account":
            if request.user.username != get_pbs_username(pbs.pbs_name):
                return redirect("App_User_Group:access-denied")
    if request.method == "POST":
        zonal_id = request.POST.get('zonal')
        item_id = request.POST.get('item')

        if Zonals_Balance.objects.filter(pbs_id=pbs_id, zonal_id=zonal_id, item_id=item_id).exclude(id=record_id).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'duplicate'})
            messages.error(request, "Update Conflict: Duplicate entry detected.")
            return redirect("PBSWise_Balance:manage_balance_view", pbs_id=pbs_id)

        try:
            # Prevent negative numbers
            deposit_work = float(request.POST.get('deposit_work', 0) or 0)
            mcep_dmd = float(request.POST.get('mcep_dmd', 0) or 0)
            mcep_kd = float(request.POST.get('mcep_kd', 0) or 0)
            mcep_bd = float(request.POST.get('mcep_bd', 0) or 0)
            other = float(request.POST.get('other', 0) or 0)
            om_store = float(request.POST.get('om_store', 0) or 0)
            own_stock = float(request.POST.get('own_stock', 0) or 0)

            if any(val < 0 for val in [deposit_work, mcep_dmd, mcep_kd, mcep_bd, other, om_store, own_stock]):
                raise ValueError("Negative values are not permitted for balance entries.")

            record.zonal_id = zonal_id
            record.item_id = item_id
            record.deposit_work = deposit_work
            record.mcep_dmd = mcep_dmd
            record.mcep_kd = mcep_kd
            record.mcep_bd = mcep_bd
            record.other = other
            record.om_store = om_store
            record.own_stock = own_stock
            record.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Record updated successfully.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, "Update failed.")

    return redirect("PBSWise_Balance:manage_balance_view", pbs_id=pbs_id)

def manage_balance_delete(request, pbs_id, record_id):
    """Delete a balance record pre-locked to a specific PBS."""
    if not check_pbs_management_permission(request.user):
        return redirect("App_User_Group:access-denied")

    record = get_object_or_404(Zonals_Balance, id=record_id, pbs_id=pbs_id)
    pbs = record.pbs

    # 🕵️ Security: For Specific_PBS_Account, only allow access to their own PBS
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.user_group.user_group_type == "Specific_PBS_Account":
            if request.user.username != get_pbs_username(pbs.pbs_name):
                return redirect("App_User_Group:access-denied")
    record.delete()
    messages.success(request, "Record removed from regional balance.")
    return redirect("PBSWise_Balance:manage_balance_view", pbs_id=pbs_id)
