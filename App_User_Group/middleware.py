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

            # Common allowed paths for restricted users
            common_allowed_paths = [
                "/home/",
                "/history/",
                "/user_group/access-denied/",
                "/accounts/logout/"
            ]

            path_for_View_History_and_Status_only = [
                "/status/",
            ]+ common_allowed_paths


            # Restriction logic
            if group_type == "View History and Status only":
                if not any(path.startswith(p) for p in path_for_View_History_and_Status_only):
                    return redirect("App_User_Group:access-denied")

            elif group_type == "Only_View_History_and_Edit_CS&M_Column":
                if not any(path.startswith(p) for p in common_allowed_paths):
                    return redirect("App_User_Group:access-denied")

            elif group_type == "Only_View_History_and_Edit_Carry_From_Warehouse_Column":
                if not any(path.startswith(p) for p in common_allowed_paths):
                    return redirect("App_User_Group:access-denied")

            elif group_type == "Editor":
                # Editor has full access → no restriction
                pass

        return self.get_response(request)
