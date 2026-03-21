from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import PBS_List, PBS_Zonals
from .all_pbs_list_page import check_editor_permission, check_pbs_management_permission

def pbs_zonals_view(request, pbs_id):
    """View to list all Zonal units for a specific PBS."""
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    zonals = PBS_Zonals.objects.filter(pbs=pbs).order_by('zonal_name')
    
    # Check if HQ already exists to constrain new selections
    has_hq = PBS_Zonals.objects.filter(pbs=pbs, zonal_type='HQ').exists()
    
    can_modify = check_editor_permission(request.user)
    can_manage_pbs = check_pbs_management_permission(request.user)
    
    context = {
        'pbs': pbs,
        'zonals': zonals,
        'has_hq': has_hq,
        'can_modify': can_modify,
        'can_manage_pbs': can_manage_pbs,
        # Sectional breakdown
        'hq_units': zonals.filter(zonal_type='HQ').order_by('zonal_name'),
        'zonal_units': zonals.filter(zonal_type='Zonal').order_by('zonal_name'),
        'sub_zonal_units': zonals.filter(zonal_type='Sub-Zonal').order_by('zonal_name'),
    }
    return render(request, "PBSWise_Templates/PBSWise_Balance/PBS_Zonals.html", context)

def pbs_zonal_add(request, pbs_id):
    """Handle adding a new Zonal unit."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to add.")
        return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)
    
    pbs = get_object_or_404(PBS_List, id=pbs_id)
    
    if request.method == "POST":
        zonal_name = request.POST.get('zonal_name', '').strip()
        zonal_type = request.POST.get('zonal_type', '').strip()
        
        if zonal_name and zonal_type:
            # Check for duplicate name in same PBS
            if PBS_Zonals.objects.filter(pbs=pbs, zonal_name__iexact=zonal_name).exists():
                messages.error(request, "This Zonal Already Exists")
                return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)

            # Re-check if it's HQ and if HQ already exists
            if zonal_type == 'HQ' and PBS_Zonals.objects.filter(pbs=pbs, zonal_type='HQ').exists():
                messages.error(request, "Error: HQ already exists for this PBS.")
            else:
                PBS_Zonals.objects.create(pbs=pbs, zonal_name=zonal_name, zonal_type=zonal_type)
                messages.success(request, f"{zonal_type} '{zonal_name}' added successfully.")
        else:
            messages.error(request, "Zonal Name and Type are required.")
            
    return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)

def pbs_zonal_edit(request, pbs_id, zonal_id):
    """Handle editing a Zonal unit."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to edit.")
        return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)
    
    zonal = get_object_or_404(PBS_Zonals, id=zonal_id, pbs_id=pbs_id)
    
    if request.method == "POST":
        zonal_name = request.POST.get('zonal_name', '').strip()
        zonal_type = request.POST.get('zonal_type', '').strip()
        
        if zonal_name and zonal_type:
            # Check for duplicate name in same PBS (excluding current)
            if PBS_Zonals.objects.filter(pbs_id=pbs_id, zonal_name__iexact=zonal_name).exclude(id=zonal_id).exists():
                messages.error(request, "This Zonal Already Exists")
                return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)

            # Check if attempting to set another HQ
            if zonal_type == 'HQ' and PBS_Zonals.objects.filter(pbs_id=pbs_id, zonal_type='HQ').exclude(id=zonal_id).exists():
                messages.error(request, "Error: Another HQ already exists for this PBS.")
            else:
                zonal.zonal_name = zonal_name
                zonal.zonal_type = zonal_type
                zonal.save()
                messages.success(request, "Zonal details updated successfully.")
        else:
            messages.error(request, "Fields cannot be empty.")
            
    return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)

def pbs_zonal_delete(request, pbs_id, zonal_id):
    """Handle deleting a Zonal unit."""
    if not check_editor_permission(request.user):
        messages.error(request, "Access Denied: You don't have permission to delete.")
        return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)
    
    zonal = get_object_or_404(PBS_Zonals, id=zonal_id, pbs_id=pbs_id)
    zonal_name = zonal.zonal_name
    zonal.delete()
    messages.success(request, f"{zonal_name} deleted successfully.")
    
    return redirect("PBSWise_Balance:pbs_zonals_view", pbs_id=pbs_id)
