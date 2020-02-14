from django.shortcuts import render

from app_projects.models import Project
from .utils import create_project_folder, setup_project


def editor(request, project_id):
    project = Project.objects.get(id=project_id)

    if(not project.project_folder):
        create_project_folder(project)
    
    setup_project(project)

    context = {
        'project': project
    }

    return render(request, 'app_editor/editor.html', context=context)