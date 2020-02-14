from django.shortcuts import render, redirect

from .models import Project
from .projects import PROJECT_TYPES, PROJECT_CATEGORIES


def list(request):
    projects = Project.objects.filter(user=request.user)

    context = {
        'projects': projects
    }

    return render(request, 'app_projects/list.html', context=context)


def create(request):
    if request.POST:
        name = request.POST['name']
        if 'description' in request.POST:
            description = request.POST['description']
        else:
            description = None
        type = request.POST['type']

        project = Project.objects.create(
            user=request.user,
            name=name,
            description=description,
            type=type
        )

        return redirect('editor:editor', project_id=project.id)
    else:
        context = {
            'project_types': PROJECT_TYPES,
            'project_categories': PROJECT_CATEGORIES,
        }
        return render(request, 'app_projects/create.html', context=context)


def delete(request, project_id):
    project = Project.objects.get(id=project_id)

    project.delete()

    return redirect('projects:list')