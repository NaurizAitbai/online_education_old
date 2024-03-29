from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_base.urls')),
    path('projects/', include('app_projects.urls')),
    path('editor/', include('app_editor.urls')),
]
