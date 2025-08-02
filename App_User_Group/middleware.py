from django.shortcuts import redirect
from App_Login.models import User_Group

class UserGroupAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info  # safer than request.path

        if request.user.is_authenticated:
            try:
                user_group = User_Group.objects.get(user=request.user)
                group_type = user_group.user_group_type
            except User_Group.DoesNotExist:
                group_type = "View History and Status only"

            # Exact paths to allow
            allowed_paths = [
                "/home/",
                "/status/",
                "/history/",
                "/user_group/access-denied/", 
                "/accounts/logout/"
            ]

            if group_type == "View History and Status only":
                if not any(path.startswith(p) for p in allowed_paths):
                    return redirect("App_User_Group:access-denied")

        return self.get_response(request)
