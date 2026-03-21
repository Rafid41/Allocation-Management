from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import PBS_List, Zonal_Items
from .all_pbs_list_page import check_pbs_management_permission, get_pbs_username
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App_Admin_Panel.models import PaginationManager

def manage_individual_pbs_zonal_home(request, pbs_id):
    """Home landing page for managing a specific PBS balance tools."""
    if not check_pbs_management_permission(request.user):
        messages.error(request, "Access Denied.")
        return redirect("App_Home:home_page")
        
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    # Security: Specific PBS Accounts can only access their own PBS
    if request.user.user_group.user_group_type == "Specific_PBS_Account":
        if request.user.username != get_pbs_username(pbs.pbs_name):
            messages.error(request, "Access Denied: Regional accounts cannot access other PBS data.")
            return redirect("PBSWise_Balance:pbs_list_view")

    context = {'pbs': pbs}
    return render(request, "PBSWise_Templates/PBSWise_Balance/manage_individual_pbs_zonals_home.html", context)

def manage_individual_pbs_zonal_items(request, pbs_id):
    """Module to manage global zonal items from a regional perspective (Add-only)."""
    if not check_pbs_management_permission(request.user):
        messages.error(request, "Access Denied.")
        return redirect("App_Home:home_page")
        
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    # Security: Validate regional account ownership
    if request.user.user_group.user_group_type == "Specific_PBS_Account":
        if request.user.username != get_pbs_username(pbs.pbs_name):
            messages.error(request, "Access Denied.")
            return redirect("PBSWise_Balance:pbs_list_view")

    # Fetch items for viewing
    search_query = request.GET.get('search', '').strip()
    if search_query:
        items_queryset = Zonal_Items.objects.filter(item_name__icontains=search_query).order_by('item_name')
    else:
        items_queryset = Zonal_Items.objects.all().order_by('item_name')

    # Fetch dynamic pagination limit from Admin Panel
    try:
        limit = PaginationManager.load().table_pagination_limit
    except:
        limit = 50 # Standard fallback

    page_number = request.GET.get('page', 1)
    paginator = Paginator(items_queryset, limit)
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except:
        page_obj = paginator.get_page(page_number)
    
    # Handle 'Add Item' action
    if request.method == "POST":
        item_name = request.POST.get('item_name', '').strip()
        if item_name:
            if Zonal_Items.objects.filter(item_name__iexact=item_name).exists():
                messages.error(request, f"Entry Error: '{item_name}' is already registered in the system.")
            else:
                Zonal_Items.objects.create(item_name=item_name)
                messages.success(request, f"Inventory Item '{item_name}' has been added to the master list.")
        else:
            messages.error(request, "Error: Item Name field cannot be blank.")
        return redirect("PBSWise_Balance:manage_individual_pbs_zonal_items", pbs_id=pbs_id)

    context = {
        'pbs': pbs,
        'items': page_obj,
        'search_query': search_query,
        'can_add': True,
        'can_edit': False, # Permission strictly enforced via view-only rendering
        'can_delete': False, 
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/manage_individual_pbs_zonals_items.html", context)
