from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from App_Allocation.models import PBS, Allocation_Number
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def allocation_page(request):
    """Renders the PBS and item entry page"""
    return render(request, "App_Allocation/allocation.html")



