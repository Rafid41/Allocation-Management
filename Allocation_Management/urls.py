from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# display media/ image
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("App_Login.urls")),
    path("accounts/", include("App_Login.urls")),
    path(
        "", lambda request: redirect("App_Login:login")
    ),  # Redirect root to /accounts/
    path("home/", include("App_Home.urls")),
    path("entry/", include("App_Entry.urls")),
    path("status/", include("App_Status.urls")),
    path("allocation/", include("App_Allocation.urls")),
]


# media / image
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
