from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import Length
from Project_App_Entry.models import Project, Project_Item
from Project_App_History.models import  Project_History
from Project_App_Allocation.models import Final_Allocation  # assuming this is where Final_Allocation is
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.decorators import login_required

login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    items = Project_Item.objects.filter(project=project).order_by("-created_at")

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

    return render(
        request,
        "Project_Templates/Project_App_ProjectWiseBalance/project_details.html",
        {"project": project, "item_data": item_data},
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
        