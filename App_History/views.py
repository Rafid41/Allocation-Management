from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from App_History.models import History
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json


@login_required
def history(request):
    results = History.objects.all().order_by('-created_at')
    applied_filters = []

    for i in range(1, 10):  # Supports up to 9 filters
        filter_type = request.GET.get(f"filter_type_{i}")
        filter_value = request.GET.get(f"filter_value_{i}")
        date_status = request.GET.get(f"date_status_{i}")

        if filter_value:
            filter_value = filter_value.strip()

        if not filter_type or filter_type == "no_condition":
            continue

        applied_filters.append({
            "type": filter_type,
            "value": filter_value,
            "date_status": date_status
        })

        # TEXT filters
        if filter_type == "allocation_no":
            results = results.filter(allocation_no__iexact=filter_value)
        elif filter_type == "pbs":
            results = results.filter(pbs__iexact=filter_value)
        elif filter_type == "package":
            results = results.filter(package__iexact=filter_value)
        elif filter_type == "item":
            results = results.filter(item__iexact=filter_value)
        elif filter_type == "warehouse":
            results = results.filter(warehouse__iexact=filter_value)
        elif filter_type == "status":
            results = results.filter(status__iexact=filter_value)

        # DATE FILTERS (CS&M or Carry)
        elif filter_type in ["cs_and_m_date", "carry_from_warehouse_date"]:
            field_name = "CS_and_M" if filter_type == "cs_and_m_date" else "carry_from_warehouse"

            # Condition set
            if not filter_value:
                # Case 1: No date selected
                if date_status == "empty":
                    # 1b. Show Empty Cells
                    results = results.filter(Q(**{f"{field_name}__isnull": True}) | Q(**{f"{field_name}__exact": ''}))
                else:
                    # 1a. Show All Data → No filter (skip)
                    pass
            else:
                # Case 2: Date is selected
                if date_status == "empty":
                    # 2b. Show records with the selected date AND also empty (which will yield nothing normally)
                    # But to strictly follow your logic: filter both equal and empty
                    results = results.filter(
                        Q(**{f"{field_name}__iexact": filter_value}) |
                        Q(**{f"{field_name}__isnull": True}) |
                        Q(**{f"{field_name}__exact": ''})
                    )
                else:
                    # 2a. Show only selected date
                    results = results.filter(**{f"{field_name}__iexact": filter_value})

    # Determine group permissions
    group = request.user.user_group.user_group_type if hasattr(request.user, "user_group") else ""

    context = {
        "items": results,
        "status_choices_json": json.dumps(History.STATUS_CHOICES),
        "can_edit_cs": group in ["Editor", "Only_View_History_and_Edit_CS&M_Column"],
        "can_edit_carry": group in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"],
        "can_edit_comments": group in ["Editor"],
    }

    return render(request, "App_History/view_and_print_history.html", context)


@login_required
@require_POST
@csrf_exempt
def update_date_view(request, id):
    try:
        data = json.loads(request.body)
        field = data.get("field")
        history = get_object_or_404(History, id=id)

        user_group_type = request.user.user_group.user_group_type
        success = False

        # Handle CS&M updates
        if field == "cs" and user_group_type in ["Editor", "Only_View_History_and_Edit_CS&M_Column"]:
            if data.get("reset"):
                history.CS_and_M = None
            else:
                date_value = data.get("date")
                if date_value:
                    history.CS_and_M = date_value
            history.save()
            success = True

        # Handle Carry updates
        elif field == "carry" and user_group_type in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"]:
            if data.get("reset"):
                history.carry_from_warehouse = None
            else:
                date_value = data.get("date")
                if date_value:
                    history.carry_from_warehouse = date_value
            history.save()
            success = True

        # Handle Comments updates
        elif field == "comments" and user_group_type in ["Editor"]:
            text_value = data.get("text", "")
            history.comments = text_value
            history.save()
            success = True

        if not success:
            return JsonResponse({"error": "Not allowed"}, status=403)

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
