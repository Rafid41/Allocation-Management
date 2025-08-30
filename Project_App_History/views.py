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
    query = request.GET.get("query", "")
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")
    date_status = request.GET.get("date_status", "all")  # <-- NEW

    results = History.objects.all().order_by('-created_at')


    # Non-date filters
    if query and filter_by not in ["allocation_date", "carry_from_warehouse_date"]:
        if filter_by == "All":
            results = results.filter(
                Q(allocation_no__icontains=query) |
                Q(pbs__icontains=query) |
                Q(project__icontains=query) |
                Q(item__icontains=query) |
                Q(warehouse__icontains=query) |
                Q(status__icontains=query) |
                Q(comments__icontains=query)
            )
        elif filter_by == "allocation_no":
            results = results.filter(allocation_no__icontains=query)
        elif filter_by == "pbs":
            results = results.filter(pbs__icontains=query)
        elif filter_by == "project":
            results = results.filter(project__icontains=query)
        elif filter_by == "item":
            results = results.filter(item__icontains=query)
        elif filter_by == "warehouse":
            results = results.filter(warehouse__icontains=query)
        elif filter_by == "status":
            results = results.filter(status__icontains=query)

    # Date filters
    if filter_by == "allocation_date":
        if date_filter:
            results = results.filter(created_at__date=date_filter)
        if date_status == "empty":
            results = results.filter(created_at__isnull=True)

    elif filter_by == "carry_from_warehouse_date":
        if date_filter:
            results = results.filter(carry_from_warehouse__date=date_filter)
        if date_status == "empty":
            results = results.filter(carry_from_warehouse__isnull=True)

    # Determine group permission
    group = request.user.user_group.user_group_type if hasattr(request.user, "user_group") else ""

    context = {
        "items": results,
        "query": query,
        "filter_by": filter_by,
        "date_filter": date_filter,
        "date_status": date_status,  # <-- Pass to template
        "can_edit_carry": group in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"],
        "can_edit_comments": group in ["Editor"],
    }

    return render(request, "Project_Templates/Project_App_History/view_and_print_history.html", context)



@login_required
@require_POST
@csrf_exempt
def update_date_view(request, id):
    try:
        data = json.loads(request.body)
        field = data.get("field")
        history = get_object_or_404(History, id=id)

        user_group_type = request.user.user_group.user_group_type

        if history.status == "Cancelled" or (history.remarks_status or "").strip().lower() == "deleted":
            return JsonResponse({"error": "Modification not allowed"}, status=403)

        if field == "carry" and user_group_type in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"]:
            if data.get("reset"):
                history.carry_from_warehouse = None
            else:
                date_value = data.get("date")
                if date_value:
                    history.carry_from_warehouse = date_value
            history.save()

        elif field == "comments" and user_group_type in ["Editor"]:
            text_value = data.get("text", "")
            history.comments = text_value
            history.save()

        else:
            return JsonResponse({"error": "Not allowed"}, status=403)

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
