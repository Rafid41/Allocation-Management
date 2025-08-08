# # App_Allocation\views\view_final_allocation.py
# from django.shortcuts import render,redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from App_Allocation.models import Final_Allocation, Allocation_Number
# from .models import History

# @login_required
# def history(request):
#     query = request.GET.get("query", "")
#     filter_by = request.GET.get("filter_by", "All")
#     date_filter = request.GET.get("date", "")

#     results = History.objects.all().order_by('-created_at')
#     # allocations_numbers = Allocation_Number.objects.all()

#     if query:
#         if filter_by == "allocation_no":
#             results = results.filter(allocation_no__icontains=query)
#         elif filter_by == "pbs":
#             results = results.filter(pbs__icontains=query)
#         elif filter_by == "package":
#             results = results.filter(package__icontains=query)
#         elif filter_by == "item":
#             results = results.filter(item__icontains=query)
#         elif filter_by == "warehouse":
#             results = results.filter(warehouse__icontains=query)
#         elif filter_by == "status":
#             results = results.filter(status__icontains=query)

#     if date_filter:
#         results = results.filter(created_at__date=date_filter)

#     context = {
#         "items": results,
#         "query": query,
#         "filter_by": filter_by,
#         "date_filter": date_filter,
#     }

#     return render(request, "App_History/view_and_print_history.html", context)


# App_Allocation/views/view_final_allocation.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from App_History.models import History
from django.views.decorators.http import require_POST
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from App_Login.models import User_Group

@login_required
def history(request):
    query = request.GET.get("query", "")
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    results = History.objects.all().order_by('-created_at')

    if query and filter_by not in ["allocation_date", "cs_and_m_date", "carry_from_warehouse_date"]:
        if filter_by == "allocation_no":
            results = results.filter(allocation_no__icontains=query)
        elif filter_by == "pbs":
            results = results.filter(pbs__icontains=query)
        elif filter_by == "package":
            results = results.filter(package__icontains=query)
        elif filter_by == "item":
            results = results.filter(item__icontains=query)
        elif filter_by == "warehouse":
            results = results.filter(warehouse__icontains=query)
        elif filter_by == "status":
            results = results.filter(status__icontains=query)

    if date_filter:
        if filter_by == "allocation_date":
            results = results.filter(created_at__date=date_filter)
        elif filter_by == "cs_and_m_date":
            results = results.filter(CS_and_M__date=date_filter)
        elif filter_by == "carry_from_warehouse_date":
            results = results.filter(carry_from_warehouse__date=date_filter)

    # Determine group permission
    group = request.user.user_group.user_group_type if hasattr(request.user, "user_group") else ""

    context = {
        "items": results,
        "query": query,
        "filter_by": filter_by,
        "date_filter": date_filter,
        "can_edit_cs": group in ["Editor", "Only_View_History_and_Edit_CS&M_Column"],
        "can_edit_carry": group in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"]
    }

    return render(request, "App_History/view_and_print_history.html", context)



@login_required
@require_POST
@csrf_exempt
def update_date_view(request, id):
    try:
        data = json.loads(request.body)
        field = data.get("field")
        date_value = data.get("date")
        history = get_object_or_404(History, id=id)

        user_group_type = request.user.user_group.user_group_type

        if field == "cs" and user_group_type in ["Editor", "Only_View_History_and_Edit_CS&M_Column"]:
            parsed_date = datetime.combine(datetime.strptime(date_value, "%Y-%m-%d").date(), time.min)
            history.CS_and_M = make_aware(parsed_date)
            history.save()
        elif field == "carry" and user_group_type in ["Editor", "Only_View_History_and_Edit_Carry_From_Warehouse_Column"]:
            parsed_date = datetime.combine(datetime.strptime(date_value, "%Y-%m-%d").date(), time.min)
            history.carry_from_warehouse = make_aware(parsed_date)
            history.save()
        else:
            return JsonResponse({"error": "Not allowed"}, status=403)

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
