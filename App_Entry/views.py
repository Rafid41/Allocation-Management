import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def entry_page(request):
    """Renders the package and item entry page"""
    return render(request, "App_Entry/entry_page.html")


# # -------------------------------------
# # PACKAGE SEARCH (AJAX)
# # -------------------------------------
# def search_packages(request):
#     """ Returns package suggestions based on search query """
#     query = request.GET.get("query", "")
#     packages = Package.objects.filter(name__icontains=query).values("id", "name")
#     return JsonResponse(list(packages), safe=False)

# # -------------------------------------
# # ITEM SEARCH (AJAX)
# # -------------------------------------
# def search_items(request):
#     """ Returns item suggestions based on search query """
#     query = request.GET.get("query", "")
#     items = Item.objects.filter(name__icontains=query).values("id", "name")
#     return JsonResponse(list(items), safe=False)

# # -------------------------------------
# # CREATE OR UPDATE PACKAGE
# # -------------------------------------
# @csrf_exempt
# def create_package(request):
#     """ Creates or updates a package based on name """
#     if request.method == "POST":
#         data = json.loads(request.body)

#         package_name = data.get("package_name")
#         warehouse = data.get("warehouse")
#         description = data.get("description", "")
#         unit = data.get("unit")

#         if not package_name:
#             return JsonResponse({"error": "Package name is required."}, status=400)

#         package, created = Package.objects.update_or_create(
#             name=package_name,
#             defaults={"warehouse": warehouse, "description": description, "unit": unit}
#         )

#         return JsonResponse({"id": package.id, "created": created})

# # -------------------------------------
# # CREATE OR UPDATE PACKAGE ITEM
# # -------------------------------------
# @csrf_exempt
# def create_package_item(request):
#     """ Adds or updates an item inside a package """
#     if request.method == "POST":
#         data = json.loads(request.body)

#         package_id = data.get("package_id")
#         item_name = data.get("item_name")
#         quantity_of_item = data.get("quantity_of_item")
#         unit_price_of_item = data.get("unit_price_of_item")

#         if not package_id or not item_name:
#             return JsonResponse({"error": "Package and Item name are required."}, status=400)

#         package = get_object_or_404(Package, id=package_id)

#         item, created = Item.objects.get_or_create(name=item_name)

#         package_item, item_created = PackageItem.objects.get_or_create(
#             package=package,
#             item=item,
#             defaults={"quantity_of_item": quantity_of_item, "unit_price_of_item": unit_price_of_item}
#         )

#         if not item_created and package_item.quantity_of_item > 0:
#             return JsonResponse({"error": "Item already exists in this package with quantity > 0."}, status=400)

#         if not item_created:
#             package_item.quantity_of_item = quantity_of_item
#             package_item.unit_price_of_item = unit_price_of_item
#             package_item.save()

#         return JsonResponse({"id": package_item.id, "updated": not item_created})
