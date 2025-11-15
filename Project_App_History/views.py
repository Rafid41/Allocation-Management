from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from Project_App_History.models import Project_History as History
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q

@login_required
def history(request):
    """
    Multi-filter history view (supports up to 9 filters).
    Text searches are exact, case-insensitive (__iexact).
    Date filters:
      - carry_from_warehouse_date: date picker + 'show empty cells' dropdown
    Note: allocation_date has been removed from the filter system.
    """
    results = History.objects.all().order_by('-created_at')
    applied_filters = []

    for i in range(1, 10):  # support up to 9 filters
        filter_type = request.GET.get(f"filter_type_{i}")
        filter_value = request.GET.get(f"filter_value_{i}")
        date_status = request.GET.get(f"date_status_{i}")

        if filter_value:
            filter_value = filter_value.strip()

        # Skip empty / no condition filters
        if not filter_type or filter_type == "no_condition" or (not filter_value and filter_type not in ["carry_from_warehouse_date"]):
            continue

        applied_filters.append({
            "type": filter_type,
            "value": filter_value,
            "date_status": date_status
        })

        # TEXT filters (exact, case-insensitive)
        if filter_type == "allocation_no":
            results = results.filter(allocation_no__iexact=filter_value)
        elif filter_type == "pbs":
            results = results.filter(pbs__iexact=filter_value)
        elif filter_type == "project":
            results = results.filter(project__iexact=filter_value)
        elif filter_type == "item":
            results = results.filter(item__iexact=filter_value)
        elif filter_type == "warehouse":
            results = results.filter(warehouse__iexact=filter_value)
        elif filter_type == "status":
            results = results.filter(status__iexact=filter_value)
        elif filter_type == "comments":
            results = results.filter(comments__iexact=filter_value)

        # DATE filters: carry_from_warehouse_date only (allocation_date removed)
        elif filter_type == "carry_from_warehouse_date":
            field_name = "carry_from_warehouse"

            # carry_from_warehouse_date logic (keeps date_status behavior)
            if not filter_value:
                if date_status == "empty":
                    results = results.filter(Q(**{f"{field_name}__isnull": True}) | Q(**{f"{field_name}__exact": ""}))
                else:
                    pass
            else:
                # Date selected
                try:
                    if date_status == "empty":
                        results = results.filter(
                            Q(**{f"{field_name}__date": filter_value}) |
                            Q(**{f"{field_name}__isnull": True}) |
                            Q(**{f"{field_name}__exact": ""})
                        )
                    else:
                        results = results.filter(**{f"{field_name}__date": filter_value})
                except Exception:
                    if date_status == "empty":
                        results = results.filter(
                            Q(**{f"{field_name}__iexact": filter_value}) |
                            Q(**{f"{field_name}__isnull": True}) |
                            Q(**{f"{field_name}__exact": ""})
                        )
                    else:
                        results = results.filter(**{f"{field_name}__iexact": filter_value})

    # Determine group permission
    group = request.user.user_group.user_group_type if hasattr(request.user, "user_group") else ""

    context = {
        "items": results,
        "status_choices_json": json.dumps(History.STATUS_CHOICES),
        "can_edit_carry": group in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"],
        "can_edit_comments": group in ["Editor"],
    }

    return render(request, "Project_Templates/Project_App_History/view_and_print_history.html", context)


@login_required
@require_POST
@csrf_exempt
def update_date_view(request, id):
    """
    Update carry_from_warehouse date or comments.
    Permissions enforced by user's group.
    Disallow modification when status == 'Cancelled' or remarks_status == 'Deleted'.
    """
    try:
        data = json.loads(request.body)
        field = data.get("field")
        history = get_object_or_404(History, id=id)

        user_group_type = request.user.user_group.user_group_type

        # Prevent modifications on cancelled/deleted rows
        if history.status == "Cancelled" or (history.remarks_status or "").strip().lower() == "deleted":
            return JsonResponse({"error": "Modification not allowed"}, status=403)

        # Handle Carry updates
        if field == "carry" and user_group_type in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"]:
            if data.get("reset"):
                history.carry_from_warehouse = None
            else:
                date_value = data.get("date")
                if date_value:
                    history.carry_from_warehouse = date_value
            history.save()
            return JsonResponse({"success": True})

        # Handle Comments updates
        elif field == "comments" and user_group_type in ["Editor"]:
            text_value = data.get("text", "")
            history.comments = text_value
            history.save()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({"error": "Not allowed"}, status=403)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
