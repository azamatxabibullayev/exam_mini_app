from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("ad/", admin.site.urls),
    path("", include("main.urls")),
    path("users/", include("users.urls")),
    path("dashboard/", include("dashboard.urls")),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('_nested_admin/', include('nested_admin.urls')),
]
