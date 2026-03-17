from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Project_App_Allocation.models import Allocation_Number
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from App_Admin_Panel.models import PaginationManager


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
                Allocation_Number.objects.create(
                    allocation_no=allocation_no,
                    user=request.user,
                    status="Pending Approval",
                )
                messages.success(
                    request, "Allocation Number added successfully!"
                )  # Success message
                return redirect(
                    reverse("Project_App_Allocation:view_allocation_numbers_and_Add_New")
                )

    # Fetch all allocation numbers to display
    all_allocation_numbers = Allocation_Number.objects.all().order_by("-allocation_no")

    # Pagination Logic
    try:
        limit = PaginationManager.load().table_pagination_limit
    except:
        limit = 50

    page_number = request.GET.get('page')
    paginator = Paginator(all_allocation_numbers, limit)
    allocation_numbers = paginator.get_page(page_number)

    return render(
        request,
        "Project_Templates/Project_App_Allocation/view_allocation_numbers_and_Add_New.html",
        {"allocation_numbers": allocation_numbers},
    )
