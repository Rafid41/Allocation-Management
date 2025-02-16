import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from App_Entry.models import Package, Item
from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.http import HttpResponse
from django.contrib import messages


def entry_page(request):
    """Renders the package and item entry page"""
    return render(request, "App_Entry/entry_page.html")


from django.urls import reverse_lazy


class PackageListAndCreate(LoginRequiredMixin, CreateView, ListView):
    model = Package
    template_name = "App_Entry/view_package_and_addNew.html"
    fields = ["packageId"]
    success_url = reverse_lazy(
        "App_Entry:view_package_and_addNew"
    )  # Redirect to the package list after form submission

    def get_queryset(self):
        return Package.objects.all().order_by("packageId")

    def form_valid(self, form):
        # Check if packageId already exists
        if Package.objects.filter(packageId=form.cleaned_data["packageId"]).exists():
            form.add_error("packageId", "This packageId already exists.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Package creation failed. Please check the errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # Add the list of packages to the context for the template
        context = super().get_context_data(**kwargs)
        context["current_package_list"] = Package.objects.all().order_by(
            "packageId"
        )  # Explicitly set the list
        return context
