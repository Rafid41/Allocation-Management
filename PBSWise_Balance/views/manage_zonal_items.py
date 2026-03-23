from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .all_pbs_list_page import check_editor_permission
from ..models import Zonal_Items
from App_Entry.models import Item as MainItem

def manage_zonal_home(request):
    """Home page for managing all zonal items and balance."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")
    
    return render(request, "PBSWise_Templates/PBSWise_Balance/manage_zonals_home.html")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App_Admin_Panel.models import PaginationManager

def manage_zonal_items(request):
    """View to manage Zonal Items (Add/Edit/Delete)."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")
    
    # Fetch all items in alphabetical order
    items_queryset = Zonal_Items.objects.all().order_by('item_name')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        items_queryset = items_queryset.filter(item_name__icontains=search_query)
    
    # Fetch dynamic pagination limit from Admin Panel
    try:
        limit = PaginationManager.load().table_pagination_limit
    except:
        limit = 50 # Fallback

    page_number = request.GET.get('page', 1)
    paginator = Paginator(items_queryset, limit)
    
    try:
        page_obj = paginator.getPage(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except: # Fallback for old paginator methods if needed
        page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,
        'search_query': search_query,
        'can_modify': True,
        'units': MainItem.UNIT_CHOICES,
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/manage_zonals_items.html", context)

def zonal_item_add(request):
    """Handle adding a Zonal Item."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")
    
    if request.method == "POST":
        item_name = request.POST.get('item_name', '').strip()
        if item_name:
            item_name = item_name[0].upper() + item_name[1:]
        unit = request.POST.get('unit', 'Nos.')
        description = request.POST.get('description', '').strip()
        if item_name:
            # Duplicate check
            if Zonal_Items.objects.filter(item_name__iexact=item_name).exists():
                messages.error(request, "This Zonal Item already exists")
                return redirect("PBSWise_Balance:manage_zonal_items")

            Zonal_Items.objects.create(item_name=item_name, unit=unit, description=description)
            messages.success(request, f"Item '{item_name}' added successfully.")
        else:
            messages.error(request, "Item name cannot be empty.")
            
    return redirect("PBSWise_Balance:manage_zonal_items")

def zonal_item_edit(request, item_id):
    """Handle editing a Zonal Item."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")
    
    item = get_object_or_404(Zonal_Items, id=item_id)
    if request.method == "POST":
        item_name = request.POST.get('item_name', '').strip()
        if item_name:
            item_name = item_name[0].upper() + item_name[1:]
        unit = request.POST.get('unit', 'Nos.')
        description = request.POST.get('description', '').strip()
        if item_name:
            # Duplicate check (excluding current item)
            if Zonal_Items.objects.filter(item_name__iexact=item_name).exclude(id=item_id).exists():
                messages.error(request, "This Zonal Item already exists")
                return redirect("PBSWise_Balance:manage_zonal_items")

            item.item_name = item_name
            item.unit = unit
            item.description = description
            item.save()
            messages.success(request, "Item updated successfully.")
        else:
            messages.error(request, "Item name cannot be empty.")
            
    return redirect("PBSWise_Balance:manage_zonal_items")

def zonal_item_delete(request, item_id):
    """Handle deleting a Zonal Item."""
    if not check_editor_permission(request.user):
        return redirect("App_User_Group:access-denied")
    
    item = get_object_or_404(Zonal_Items, id=item_id)
    item_name = item.item_name
    item.delete()
    messages.success(request, f"Item '{item_name}' and all related data deleted.")
    
    return redirect("PBSWise_Balance:manage_zonal_items")
