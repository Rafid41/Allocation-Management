from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from PBSWise_Balance.models import PBS_List, PBS_Zonals, Zonal_Items, Zonals_Balance
from PBSWise_History.models import PBS_History
from App_Admin_Panel.models import PaginationManager

from PBSWise_Balance.views.all_pbs_list_page import get_pbs_username

def inventory_management_view(request, pbs_id):
    """
    Main view for Transfer and Withdrawal of items across Zones within a PBS.
    Also shows a searchable list of current balances.
    """
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    # 🕵️ Security: For Specific_PBS_Account, only allow access to their own PBS
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.user_group.user_group_type == "Specific_PBS_Account":
            if request.user.username != get_pbs_username(pbs.pbs_name):
                return redirect("App_User_Group:access-denied")
    
    # Store Choices
    STORE_CHOICES = [
        ('deposit_work', 'Deposit Work'),
        ('mcep_dmd', 'MCEP-DMD'),
        ('mcep_kd', 'MCEP-KD'),
        ('mcep_bd', 'MCEP-BD'),
        ('other', 'Other'),
        ('om_store', 'O&M Store'),
        ('own_stock', 'Own Stock'),
    ]

    if request.method == 'POST':
        action = request.POST.get('action')
        zonal_from_id = request.POST.get('zonal_from')
        store_from = request.POST.get('store_from')
        zonal_to_id = request.POST.get('zonal_to')
        store_to = request.POST.get('store_to')
        item_id = request.POST.get('item')
        try:
            quantity = float(request.POST.get('quantity', 0))
        except ValueError:
            quantity = 0

        if not action or action == "Select an option":
            messages.error(request, "Please select an Action.")
        elif not item_id or item_id == "Select an option":
            messages.error(request, "Please select an Item.")
        elif quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
        else:
            try:
                with transaction.atomic():
                    # 1. Fetch Source Record
                    source_record = Zonals_Balance.objects.select_for_update().get(
                        pbs=pbs,
                        zonal_id=zonal_from_id,
                        item_id=item_id
                    )
                    
                    current_source_val = getattr(source_record, store_from) or 0
                    
                    if quantity > current_source_val:
                        messages.error(request, f"Quantity exceeds available stock in {store_from.replace('_', ' ').title()} ({current_source_val}).")
                    else:
                        # Deduct from Source
                        setattr(source_record, store_from, current_source_val - quantity)
                        source_record.save()
                        
                        if action == "Transfer Item":
                            # 2. Fetch or Create Destination Record
                            dest_record, created = Zonals_Balance.objects.select_for_update().get_or_create(
                                pbs=pbs,
                                zonal_id=zonal_to_id,
                                item_id=item_id
                            )
                            current_dest_val = getattr(dest_record, store_to) or 0
                            setattr(dest_record, store_to, current_dest_val + quantity)
                            dest_record.save()
                        
                        # 3. Log to History
                        PBS_History.objects.create(
                            pbs=pbs,
                            item=source_record.item,
                            quantity=quantity,
                            action=action,
                            zonal_from_id=zonal_from_id,
                            store_from=store_from,
                            zonal_to_id=zonal_to_id if action == "Transfer Item" else None,
                            store_to=store_to if action == "Transfer Item" else None
                        )

                        if action == "Transfer Item":
                            messages.success(request, f"Successfully transferred {quantity} units to {dest_record.zonal.zonal_name} ({store_to.replace('_', ' ').title()}).")
                        else:
                            messages.success(request, f"Successfully withdrew {quantity} units from {source_record.zonal.zonal_name} ({store_from.replace('_', ' ').title()}).")
                        
                        return redirect('PBSWise_Inventory:inventory_management_view', pbs_id=pbs_id)
            except Zonals_Balance.DoesNotExist:
                messages.error(request, "Source record not found in database.")
            except Exception as e:
                messages.error(request, f"Error processing transaction: {str(e)}")

    # --- GET Logic: Search and Table ---
    queryset = Zonals_Balance.objects.filter(pbs=pbs).select_related('zonal', 'item').order_by('zonal__zonal_name', 'item__item_name')
    
    # Search Parameters
    search_query = request.GET.get('search', '').strip()
    zonal_search_id = request.GET.get('zonal_id', '').strip()
    item_search_name = request.GET.get('item_name', '').strip()

    if search_query:
        queryset = queryset.filter(
            Q(item__item_name__icontains=search_query) |
            Q(zonal__zonal_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if zonal_search_id:
        queryset = queryset.filter(zonal_id=zonal_search_id)
    if item_search_name:
        queryset = queryset.filter(item__item_name=item_search_name)

    # Unique Zonals and Item Names FOR SEARCH (from current PBS data)
    zonals_search = queryset.filter(pbs=pbs).values('zonal__id', 'zonal__zonal_name').distinct().order_by('zonal__zonal_name')
    items_search = queryset.filter(pbs=pbs).values_list('item__item_name', flat=True).distinct().order_by('item__item_name')

    # Dynamic pagination limit
    try:
        limit = PaginationManager.load().table_pagination_limit
    except:
        limit = 50

    paginator = Paginator(queryset, limit)
    page_number = request.GET.get('page', 1)
    try:
        items = paginator.page(page_number)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    # Context for Form
    zonals = PBS_Zonals.objects.filter(pbs=pbs).order_by('zonal_name')
    
    context = {
        'pbs': pbs,
        'items': items,
        'search_query': search_query,
        'zonal_search_id': zonal_search_id,
        'item_search_name': item_search_name,
        'zonals': zonals,
        'zonals_search': zonals_search,
        'items_search': items_search,
        'store_choices': STORE_CHOICES,
    }
    return render(request, "PBSWise_Templates/PBSWise_Inventory/inventory_management.html", context)

def get_items_for_zonal_ajax(request):
    """AJAX helper to fetch items that have balance records in a specific zonal."""
    zonal_id = request.GET.get('zonal_id')
    pbs_id = request.GET.get('pbs_id')
    
    if not zonal_id or not pbs_id:
        return JsonResponse({'items': []})
    
    # We want items that exist in Zonals_Balance for this specific Zonal/PBS
    balance_records = Zonals_Balance.objects.filter(pbs_id=pbs_id, zonal_id=zonal_id).select_related('item').order_by('item__item_name')
    
    items_data = []
    for rec in balance_records:
        items_data.append({
            'id': rec.item.id,
            'name': rec.item.item_name,
            # We can also pass the current stock values if needed for client-side validation
            'stocks': {
                'deposit_work': float(rec.deposit_work or 0),
                'mcep_dmd': float(rec.mcep_dmd or 0),
                'mcep_kd': float(rec.mcep_kd or 0),
                'mcep_bd': float(rec.mcep_bd or 0),
                'other': float(rec.other or 0),
                'om_store': float(rec.om_store or 0),
                'own_stock': float(rec.own_stock or 0),
            }
        })
    
    return JsonResponse({'items': items_data})
