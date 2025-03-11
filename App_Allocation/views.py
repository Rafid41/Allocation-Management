from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import PBS, Allocation_Number
from django.urls import reverse
from django.contrib import messages


# Create your views here.
@login_required
def allocation_page(request):
    """Renders the PBS and item entry page"""
    return render(request, "App_Allocation/allocation.html")


@login_required
def view_PBS_and_addNew(request):
    """Handles both displaying the PBS list and adding a new PBS."""

    if request.method == "POST":
        PBS_name = request.POST.get("PBS_Name")  # Fix: Match HTML form field name

        if PBS_name:
            PBS_name = PBS_name.strip()  # Remove extra spaces
            if PBS.objects.filter(name=PBS_name).exists():
                messages.error(
                    request, "This PBS already exists!"
                )  # Show error message
            else:
                PBS.objects.create(name=PBS_name)
                messages.success(
                    request, "PBS added successfully!"
                )  # Show success message
                return HttpResponseRedirect(
                    reverse("App_Allocation:view_PBS_and_addNew")
                )

    # Fetch all PBSs to display
    PBSs = PBS.objects.all().order_by("name")

    return render(
        request,
        "App_Allocation/view_PBS_and_addNew.html",
        {"current_PBS_list": PBSs},
    )


@login_required
def view_allocation_numbers_and_Add_New(request):
    """Handles both displaying the Allocation_Number list and adding a new one."""

    if request.method == "POST":
        allocation_no = request.POST.get("allocation_no")  # Get input from form

        if allocation_no:
            allocation_no = allocation_no.strip()  # Remove extra spaces
            if Allocation_Number.objects.filter(allocation_no=allocation_no).exists():
                messages.error(
                    request, "This Allocation Number already exists!"
                )  # Error message
            else:
                Allocation_Number.objects.create(allocation_no=allocation_no)
                messages.success(
                    request, "Allocation Number added successfully!"
                )  # Success message
                return redirect(
                    reverse("App_Allocation:view_allocation_numbers_and_Add_New")
                )

    # Fetch all allocation numbers to display
    allocation_numbers = Allocation_Number.objects.all().order_by("allocation_no")

    return render(
        request,
        "App_Allocation/view_allocation_numbers_and_Add_New.html",
        {"allocation_numbers": allocation_numbers},
    )


# ########################  Search & Select for Allocation ##########################
from django.shortcuts import render
from App_Entry.models import Item
from django.db.models import Q
from datetime import datetime


@login_required
def Search_and_Select(request):
    """Renders the package and item entry page with search functionality"""
    query = request.GET.get(
        "query", ""
    ).strip()  # Strip leading/trailing whitespaces from query input
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    items = Item.objects.all()

    # Apply query filter based on the selected 'filter_by' option
    if query:
        if filter_by == "All":
            items = items.filter(
                Q(name__icontains=query)
                | Q(package__packageId__icontains=query)
                | Q(warehouse__icontains=query)
                | Q(unit_of_item__icontains=query)
            )
        elif filter_by == "Package ID":
            items = items.filter(package__packageId__icontains=query)
        elif filter_by == "Item Name":
            items = items.filter(name__icontains=query)
        elif filter_by == "Warehouse":
            items = items.filter(warehouse__icontains=query)
        elif filter_by == "Unit":
            items = items.filter(unit_of_item__icontains=query)

    # Apply date filter only if "Entry/Update date" is selected
    if filter_by == "Entry/Update date" and date_filter:
        try:
            # Ensure the date format matches
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            items = items.filter(created_at__date=date_obj.date())
        except ValueError:
            pass  # If the date format is invalid, ignore the filter

    # Order the results by package ID
    items = items.order_by("package__packageId")

    return render(
        request,
        "App_Allocation/Search_and_Select.html",
        {
            "items": items,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
        },
    )


# ########################  Allocate to PBS ##########################
from django.http import JsonResponse
from .models import Temporary_Allocation, PBS, Package, Item
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Temporary_Allocation, Item, Final_Allocation
from .forms import TemporaryAllocationForm


# def validate_allocation_no(request):
#     """Check if the allocation number already exists."""
#     allocation_no = request.GET.get("allocation_no")
#     exists = Temporary_Allocation.objects.filter(allocation_no=allocation_no).exists()
#     return JsonResponse({"exists": exists})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, PBS, Temporary_Allocation
from .forms import TemporaryAllocationForm


@login_required
def allocate_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    pbss = PBS.objects.all()  # Fetch all PBS options

    if request.method == "POST":
        form = TemporaryAllocationForm(request.POST)
        pbs_id = request.POST.get("pbs")  # Get selected PBS ID from form
        allocation_no = request.POST.get("allocation_no")  # Get allocation number
        quantity = request.POST.get("quantity")  # Get quantity

        # Convert quantity to integer safely
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity entered.")
            return redirect("App_Allocation:allocate_item", item_id=item.id)

        # Validate Allocation Number
        allocation_exists = (
            Temporary_Allocation.objects.filter(allocation_no=allocation_no).exists()
            or Final_Allocation.objects.filter(allocation_no=allocation_no).exists()
        )

        if allocation_exists:
            messages.error(
                request,
                "Allocation Number Already Exists in Temporary or Final Allocation.",
            )
        elif quantity > item.quantity_of_item:
            messages.error(request, "Entered quantity exceeds available stock!")
        elif not pbs_id:
            messages.error(request, "Please select a valid PBS before submitting.")
        else:
            allocation = form.save(commit=False)
            allocation.item = item
            allocation.item_primary_key = item.id
            allocation.package = item.package
            allocation.warehouse = item.warehouse
            allocation.price = item.unit_price
            allocation.pbs = get_object_or_404(PBS, id=pbs_id)  # Assign PBS
            allocation.save()
            messages.success(request, "Item allocated successfully!")
            return redirect("App_Allocation:Search_and_Select")

    else:
        form = TemporaryAllocationForm(
            initial={
                "package": item.package,
                "warehouse": item.warehouse,
                "unit": item.unit_of_item,
                "unit_price": item.unit_price,
            }
        )

    # Fetch Temporary Allocations sorted by Allocation number
    allocations = Temporary_Allocation.objects.all().order_by("allocation_no")

    return render(
        request,
        "App_Allocation/allocate_item.html",
        {
            "form": form,
            "item": item,
            "pbss": pbss,
            "allocations": allocations,
        },
    )


# ########################  Confirm Allocation ##########################
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q  # Import Q for complex queries
from .models import Temporary_Allocation, PBS, Package, Item
from django.contrib.auth.decorators import login_required


@login_required
def delete_allocation(request, allocation_id):
    allocation = get_object_or_404(Temporary_Allocation, id=allocation_id)
    allocation.delete()
    messages.success(request, "Allocation deleted successfully.")
    return redirect("App_Allocation:confirm_allocation_view")


from datetime import datetime


@login_required
def confirm_allocation_view(request):
    query = request.GET.get("query", "").strip()
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date_filter", "")

    allocations = Temporary_Allocation.objects.all()

    # Apply query filters based on the filter_by field
    if query:
        if filter_by == "allocation_no":
            allocations = allocations.filter(allocation_no__icontains=query)
        elif filter_by == "pbs":
            allocations = allocations.filter(pbs__name__icontains=query)
        elif filter_by == "package":
            allocations = allocations.filter(package__packageId__icontains=query)
        elif filter_by == "item":
            allocations = allocations.filter(item__name__icontains=query)
        elif filter_by == "warehouse":
            allocations = allocations.filter(warehouse__icontains=query)
        elif filter_by == "All":
            # For the "All" filter, search across multiple fields
            allocations = allocations.filter(
                Q(allocation_no__icontains=query)
                | Q(pbs__name__icontains=query)
                | Q(package__packageId__icontains=query)
                | Q(item__name__icontains=query)
                | Q(warehouse__icontains=query)
                | Q(price__icontains=query)
                | Q(quantity__icontains=query)
            )

    # Handle filtering by "Entry/Update date"
    if filter_by == "Entry/Update date" and date_filter:
        try:
            # Convert the date string to a datetime object and filter by the created_at field
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            allocations = allocations.filter(created_at__date=date_obj.date())
        except ValueError:
            # If the date string is not valid, ignore the filter
            pass

    # Sort the allocations by allocation_no
    allocations = allocations.order_by("allocation_no")

    context = {
        "allocations": allocations,
        "query": query,
        "filter_by": filter_by,
        "date_filter": date_filter,
    }

    return render(request, "App_Allocation/confirm_allocation.html", context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Temporary_Allocation, Item, Final_Allocation
from django.contrib.auth.decorators import login_required


@login_required
def confirm_allocation(request, allocation_id):
    # Get the selected allocation
    allocation = get_object_or_404(Temporary_Allocation, id=allocation_id)
    item = allocation.item

    # Check if the item quantity is sufficient
    if item.quantity_of_item >= allocation.quantity:
        # If sufficient, create an entry in Final_Allocation
        final_allocation = Final_Allocation.objects.create(
            allocation_no=allocation.allocation_no,
            item_primary_key=allocation.item_primary_key,
            pbs=allocation.pbs,
            package=allocation.package,
            item=allocation.item,
            warehouse=allocation.warehouse,
            quantity=allocation.quantity,
            price=allocation.price,
        )

        # Update item quantity in Item table
        item.quantity_of_item -= allocation.quantity
        item.save()

        # Delete the temporary allocation
        allocation.delete()

        # Display success message
        messages.success(
            request,
            f"Allocation {allocation.allocation_no} confirmed and transferred to Final Allocation and Entry for Temporary Allocation is Deleted.",
        )
    else:
        # If quantity exceeds, show error message
        messages.error(
            request, f"Quantity exceeds available stock for item {item.name}."
        )

    # Redirect to the confirmation page
    return redirect("App_Allocation:confirm_allocation_view")


# ########################  Search & Print for Final Allocation ##########################
from django.shortcuts import render
from App_Allocation.models import Final_Allocation
from django.db.models import Q
from datetime import datetime


def view_final_allocation(request):
    """Renders the Final Allocation search and print page"""

    query = request.GET.get("query", "").strip()
    filter_by = request.GET.get("filter_by", "All")
    date_filter = request.GET.get("date", "")

    allocations = Final_Allocation.objects.all()

    # Apply query filter based on the selected 'filter_by' option
    if query:
        if filter_by == "All":
            allocations = allocations.filter(
                Q(allocation_no__icontains=query)
                | Q(pbs__name__icontains=query)  # Assuming PBS has a 'name' field
                | Q(package__packageId__icontains=query)
                | Q(item__name__icontains=query)
                | Q(warehouse__icontains=query)
            )
        elif filter_by == "Allocation No":
            allocations = allocations.filter(allocation_no__icontains=query)
        elif filter_by == "PBS":
            allocations = allocations.filter(pbs__name__icontains=query)
        elif filter_by == "Package":
            allocations = allocations.filter(package__packageId__icontains=query)
        elif filter_by == "Item":
            allocations = allocations.filter(item__name__icontains=query)
        elif filter_by == "Warehouse":
            allocations = allocations.filter(warehouse__icontains=query)

    # Apply date filter
    if filter_by == "Entry/Update date" and date_filter:
        try:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d")
            allocations = allocations.filter(created_at__date=date_obj.date())
        except ValueError:
            pass  # Ignore invalid date formats

    # Order by allocation_no
    allocations = allocations.order_by("allocation_no")

    return render(
        request,
        "App_Allocation/view_print_Final_allocation.html",
        {
            "allocations": allocations,
            "query": query,
            "filter_by": filter_by,
            "date_filter": date_filter,
        },
    )
