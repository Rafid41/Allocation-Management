from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import PBS
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
                messages.error(request, "This PBS already exists!")  # Show error message
            else:
                PBS.objects.create(name=PBS_name)
                messages.success(request, "PBS added successfully!")  # Show success message
                return HttpResponseRedirect(reverse("App_Allocation:view_PBS_and_addNew"))

    # Fetch all PBSs to display
    PBSs = PBS.objects.all().order_by("name")

    return render(
        request,
        "App_Allocation/view_PBS_and_addNew.html",
        {"current_PBS_list": PBSs},
    )