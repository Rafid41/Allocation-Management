import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from App_Entry.models import Package, Item
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    View,
    TemplateView,
    DeleteView,
)
from django import forms
from django.contrib import messages
from django.urls import reverse


def entry_page(request):
    """Renders the package and item entry page"""
    return render(request, "App_Entry/entry_page.html")


from django.urls import reverse_lazy


##################################  view package and add new Package #################################
@login_required
def view_package_and_addNew(request):
    """Handles both displaying the package list and adding a new package."""

    if request.method == "POST":
        package_id = request.POST.get("packageId")

        if package_id:
            # Ensure packageId is a valid integer
            try:
                package_id = int(package_id)
                if Package.objects.filter(packageId=package_id).exists():
                    messages.error(request, "This package ID already exists!")
                else:
                    Package.objects.create(packageId=package_id)
                    messages.success(request, "Package added successfully!")
                    return HttpResponseRedirect(
                        reverse("App_Entry:view_package_and_addNew")
                    )
            except ValueError:
                messages.error(request, "Invalid package ID. Please enter a number.")

    # Fetch all packages to display
    packages = Package.objects.all().order_by("packageId")

    return render(
        request,
        "App_Entry/view_package_and_addNew.html",
        {"current_package_list": packages},
    )


############################## Add New Item to a Package ##########################################
def add_item_to_pkg(request):
    """Renders the package and item entry page"""
    return render(request, "App_Entry/Add_item_to_package.html")
