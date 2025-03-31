from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from App_Allocation.models import PBS, Allocation_Number
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


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
                    reverse("App_Allocation:view_allocation_numbers_and_Add_New")
                )

    # Fetch all allocation numbers to display
    allocation_numbers = Allocation_Number.objects.all().order_by("-allocation_no")

    return render(
        request,
        "App_Allocation/view_allocation_numbers_and_Add_New.html",
        {"allocation_numbers": allocation_numbers},
    )
