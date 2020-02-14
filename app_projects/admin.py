from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'description']
    list_display = ['name']
    search_fields = ['user__username', 'name', 'description']