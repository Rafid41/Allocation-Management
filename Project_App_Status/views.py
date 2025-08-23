from django.shortcuts import render, get_object_or_404
from Project_App_Entry.models import Project_Item as Item
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def status_page(request):
    """Renders the project and item entry page with search functionality"""
    query = request.GET.get("query", "").strip()
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    items = Item.objects.all()

    # Apply query filter based on the selected 'filter_by' option
    if query:
        if filter_by == "All":
            items = items.filter(
                Q(name__icontains=query)
                | Q(project__projectId__icontains=query)
                | Q(warehouse__icontains=query)
                | Q(unit_of_item__icontains=query)
                | Q(comments__icontains=query)
            )
        elif filter_by == "Project ID":
            items = items.filter(project__projectId__icontains=query)
        elif filter_by == "Item Name":
            items = items.filter(name__icontains=query)
        elif filter_by == "Warehouse":
            items = items.filter(warehouse__icontains=query)
        elif filter_by == "Unit":
            items = items.filter(unit_of_item__icontains=query)

    # Apply date filter only if "Entry/Update date" is selected
    if filter_by == "Entry/Update date" and date_filter:
        try:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            items = items.filter(created_at__date=date_obj.date())
        except ValueError:
            pass

    # Order the results by project ID
    items = items.order_by("project__projectId")

    # Determine group permission
    group = request.user.user_group.user_group_type if hasattr(request.user, "user_group") else ""

    context = {
        "items": items,
        "query": query,
        "filter_by": filter_by,
        "date_filter": date_filter,
        "can_edit_comments": group == "Editor",
    }

    return render(request, "Project_Templates/Project_App_Status/status.html", context)


@login_required
@require_POST
@csrf_exempt
def update_comment(request, id):
    """Update comment for a specific item (Editors only)"""
    try:
        if not hasattr(request.user, "user_group") or request.user.user_group.user_group_type != "Editor":
            return JsonResponse({"error": "Not allowed"}, status=403)

        data = json.loads(request.body)
        text_value = data.get("text", "")

        item = get_object_or_404(Item, id=id)
        item.comments = text_value
        item.save()
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
