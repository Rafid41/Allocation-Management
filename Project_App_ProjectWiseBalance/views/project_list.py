from django.shortcuts import render, get_object_or_404
from Project_App_Entry.models import Project

def project_list(request):
    projects = Project.objects.all().order_by('-projectId')  # descending order
    return render(request, "Project_Templates/Project_App_ProjectWiseBalance/project_list.html", {"projects": projects})