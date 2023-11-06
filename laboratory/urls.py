"""
Main urls
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('core.urls')),
    path('analysis/', include('analysis.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
