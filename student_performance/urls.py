from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin-panel/", include("custom_admin.urls")),  # ✅ Custom admin
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('students/', include('students.urls')),
]
