from django.shortcuts import render, get_object_or_404
from Project_App_Allocation.models import Allocation_Number

def modification_options(request, allocation_id):
    allocation = get_object_or_404(Allocation_Number, id=allocation_id)
    return render(request, "Project_Templates/Project_App_Modification/modification_options.html", {
        "allocation": allocation
    })
