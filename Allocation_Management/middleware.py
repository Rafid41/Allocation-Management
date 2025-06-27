# Allocation_Management\middleware.py

from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = '/accounts/login/'

        # Allow access if user is authenticated, or if the path is login page or static/media files
        if not request.user.is_authenticated:
            if (request.path_info != login_url and
                not request.path_info.startswith('/static/') and
                not request.path_info.startswith('/media/')):
                return redirect(login_url)

        response = self.get_response(request)
        return response


import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get login time from session or store it if not set
            login_time = request.session.get('login_time')

            if login_time:
                login_time = datetime.datetime.fromisoformat(login_time)
                elapsed = now() - login_time
                
                if elapsed.total_seconds() > 12 * 3600:  # 12 hours
                    logout(request)
            else:
                # Store login time as ISO format string
                request.session['login_time'] = now().isoformat()

        response = self.get_response(request)
        return response
