from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def allocation_page(request):
    """Renders the PBS and item entry page"""
    return render(request, "Project_Templates/Project_App_Allocation/allocation.html")



