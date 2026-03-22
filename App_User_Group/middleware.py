from django.shortcuts import redirect
from App_Login.models import User_Group

class UserGroupAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info  # safer than request.path

        # --- Restrict a specific path for ALL users ---
        restricted_paths_for_all = [
            "/project/project_allocation/final-allocation/individual-download/", 
        ]
        if any(path.startswith(p) for p in restricted_paths_for_all):
            return redirect("App_User_Group:access-denied")

        if request.user.is_authenticated:
            # Superusers have full institutional access across all portals
            if request.user.is_superuser:
                return self.get_response(request)

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
                "/accounts/logout/",
                # Project-related paths
                "/project/",
            ]

            path_for_View_History_and_Status_only = [
                "/status/",
                "/pbswise/home/",
                "/pbswise/PBS_Summary/",
                "/pbswise/storeWise_balance/",
                "/pbswise/get_summary_suggestions_ajax/",
            ] + common_allowed_paths

            # Restriction logic per user group
            if group_type == "View History and Status only":
                # Block specific PBSWise sectors (Inverse of allowed)
                blocked_pbswise_paths = [
                    "/pbswise/pbswise_balance/",
                    "/pbswise/pbswise_inventory/",
                    "/pbswise/pbswise_history/",
                ]
                if any(path.startswith(p) for p in blocked_pbswise_paths):
                    return redirect("App_User_Group:access-denied")

                restricted_subpaths = [               
                    "/project/project_allocation/",
                    "/project/project_modification/",
                    "/project/project_cancellation/",
                    "/project/project_entry/",
                    "/project/project_wise_balance/projects/"
                ]
                # If restricted path matches, block immediately
                if any(path.startswith(p) for p in restricted_subpaths):
                    return redirect("App_User_Group:access-denied")
                
                if not any(path.startswith(p) for p in path_for_View_History_and_Status_only):
                    return redirect("App_User_Group:access-denied")

            elif group_type in ["Only_View_History_and_Edit_CS&M_Column",
                                "Only_View_History_and_Edit_Carry_From_Warehouse_Column"]:
                # Block absolute access to /pbswise/
                if path.startswith("/pbswise/"):
                    return redirect("App_User_Group:access-denied")

                restricted_subpaths = [               
                    "/project/project_allocation/",
                    "/project/project_status/",
                    "/project/project_modification/",
                    "/project/project_cancellation/",
                    "/project/project_entry/",
                    "/project/project_wise_balance/projects/"
                ]
                # If restricted path matches, block immediately
                if any(path.startswith(p) for p in restricted_subpaths):
                    return redirect("App_User_Group:access-denied")
                
                if not any(path.startswith(p) for p in common_allowed_paths):
                    return redirect("App_User_Group:access-denied")

            elif group_type == "Specific_PBS_Account":
                # Block institutional reporting sectors
                blocked_pbswise_paths = [
                    "/pbswise/PBS_Summary/",
                    "/pbswise/storeWise_balance/",
                    "/pbswise/pbswise_history/",
                ]
                if any(path.startswith(p) for p in blocked_pbswise_paths):
                    return redirect("App_User_Group:access-denied")

                # Strictly PBSWise Home & Regional Tools only
                allowed_prefixes = [
                    "/pbswise/",
                    "/accounts/logout/", # Required for exit
                    "/user_group/access-denied/", # Required for the error page itself
                ]
                if not any(path.startswith(p) for p in allowed_prefixes):
                    return redirect("App_User_Group:access-denied")

            elif group_type == "Editor" or request.user.is_superuser:
                # Editor and Superuser have full access → no restriction
                pass

        return self.get_response(request)
