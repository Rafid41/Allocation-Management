from django.shortcuts import render

# Create your views here.

def home_page(request):
    """View to render the PBS-Wise Home Page."""
    return render(request, "PBSWie_Templates/PBSWise_Home/PBSWise_home_page.html")
