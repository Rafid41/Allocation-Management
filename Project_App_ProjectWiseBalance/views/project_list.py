from django.shortcuts import render, get_object_or_404
from Project_App_Entry.models import Project
from django.core.paginator import Paginator
from App_Admin_Panel.models import PaginationManager

def project_list(request):
    all_projects = Project.objects.all().order_by('-projectId')  # descending order
    
    # Pagination Logic
    try:
        limit = PaginationManager.load().table_pagination_limit
    except:
        limit = 50

    page_number = request.GET.get('page')
    paginator = Paginator(all_projects, limit)
    projects = paginator.get_page(page_number)
    
    return render(request, "Project_Templates/Project_App_ProjectWiseBalance/project_list.html", {"projects": projects})