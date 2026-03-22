from django.shortcuts import render
# Reusing the PBS_List from PBSWise_Balance as it contains the canonical list of regions
from PBSWise_Balance.models import PBS_List
from App_Login.models import User_Group
from PBSWise_Balance.views.all_pbs_list_page import get_pbs_username

def pbs_list_view(request):
    """View to list all PBS items for Inventory Management (Read-only)."""
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        pbs_items = PBS_List.objects.filter(pbs_name__icontains=search_query).order_by('pbs_name')
    else:
        pbs_items = PBS_List.objects.all().order_by('pbs_name')
    
    # 🕵️ Security: For Specific_PBS_Account, only show their own PBS entry
    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            user_group = User_Group.objects.get(user=request.user)
            if user_group.user_group_type == "Specific_PBS_Account":
                # Filter locally to match the generated username pattern
                pbs_items = [pbs for pbs in pbs_items if get_pbs_username(pbs.pbs_name) == request.user.username]
        except User_Group.DoesNotExist:
            pass

    # We pass 'can_modify' as False to ensure the template hides all Add/Edit/Delete UI
    context = {
        'pbs_items': pbs_items,
        'search_query': search_query,
        'can_modify': False, 
    }
    return render(request, "PBSWise_Templates/PBSWise_Inventory/pbs_lists.html", context)
