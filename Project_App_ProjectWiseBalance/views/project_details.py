from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from django.db.models.functions import Length
from Project_App_Entry.models import Project, Project_Item
from Project_App_History.models import  Project_History
from Project_App_Allocation.models import Final_Allocation  # assuming this is where Final_Allocation is
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.decorators import login_required
import json # Import json

@login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    items = Project_Item.objects.filter(project=project).order_by("-created_at")

    applied_filters = []

    for i in range(1, 6):  # Supports up to 5 filters
        filter_type = request.GET.get(f"filter_type_{i}")
        filter_value = request.GET.get(f"filter_value_{i}")
        date_status = request.GET.get(f"date_status_{i}") # For date fields

        if filter_value:
            filter_value = filter_value.strip()

        # Skip empty or no-condition filters
        if not filter_type or filter_type == "no_condition" or (not filter_value and filter_type != "entry_update_date"):
            continue

        applied_filters.append({
            "type": filter_type,
            "value": filter_value,
            "date_status": date_status
        })

        if filter_type == "item_name":
            items = items.filter(name__iexact=filter_value)
        elif filter_type == "warehouse":
            items = items.filter(warehouse__iexact=filter_value)
        elif filter_type == "unit":
            items = items.filter(unit_of_item__iexact=filter_value)
        elif filter_type == "entry_update_date":
            if filter_value: # Only filter if a date is provided
                items = items.filter(created_at__date__iexact=filter_value)

    item_data = []

    for item in items:
        # --- 5. Allocated ---
        allocated_sum = (
            Final_Allocation.objects.filter(project=project, item=item)
            .aggregate(total=Sum("quantity"))["total"]
            or 0
        )
        allocated_sum = Decimal(allocated_sum).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)

        # --- 6. Carried ---
        carried_sum = (
            Project_History.objects.filter(
                project=str(project.projectId),
                item_primary_key=item.id,
            )
            .exclude(status="Cancelled")
            .exclude(remarks_status="Deleted")
            .filter(carry_from_warehouse__isnull=False)
            .annotate(carry_len=Length('carry_from_warehouse'))
            .filter(carry_len__gte=6)
            .aggregate(total=Sum("quantity"))["total"]
            or 0
        )
        carried_sum = Decimal(carried_sum).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)

        # --- 7. Uncarried ---
        uncarried = Decimal(allocated_sum - carried_sum).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)

        # --- 8. Balance with Uncarried ---
        balance_with_uncarried = Decimal(item.quantity_of_item + uncarried).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)

        # --- 10. Remarks ---
        remarks = item.remarks_for_projectWiseBalance or ""

        item_data.append({
            "name": item.name,
            "warehouse": item.warehouse,
            "unit": item.unit_of_item,
            "quantity": Decimal(item.quantity_of_item).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP),
            "allocated": allocated_sum,
            "carried": carried_sum,
            "uncarried": uncarried,
            "balance": balance_with_uncarried,
            "created_at": item.created_at,
            "remarks": remarks,
            "id": item.id,
        })

    context = {
        "project": project,
        "item_data": item_data,
        "warehouse_choices_json": json.dumps(Project_Item.WAREHOUSE_CHOICES),
        "unit_choices_json": json.dumps(Project_Item.UNIT_CHOICES),
        "applied_filters_json": json.dumps(applied_filters),
    }

    return render(
        request,
        "Project_Templates/Project_App_ProjectWiseBalance/project_details.html",
        context,
    )



from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

@login_required
@require_POST
def update_remarks(request, item_id):
    if request.user.user_group.user_group_type != "Editor":
        return JsonResponse({"error": "Permission denied"}, status=403)

    try:
        data = json.loads(request.body)
        remarks = data.get("remarks", "")

        item = get_object_or_404(Project_Item, id=item_id)
        item.remarks_for_projectWiseBalance = remarks
        item.save()

        return JsonResponse({"success": True, "remarks": remarks})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
        