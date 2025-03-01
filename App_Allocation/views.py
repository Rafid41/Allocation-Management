from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
@login_required
def allocation_page(request):
    """Renders the package and item entry page"""
    return render(request, "App_Allocation/allocation.html")
