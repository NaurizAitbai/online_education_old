import os.path
import shutil

from django.conf import settings


def create_project_folder(project):
    project.project_identifier = 'pr-{}-{}'.format(project.id, project.name[:10])

    project_folder = os.path.join(
        settings.BASE_DIR,
        'uploads',
        'projects',
        '{}-{}'.format(project.user.username[:15], user.id),
        project.project_identifier
    )

    project.project_folder = project_folder
    project.save()

    return project_folder


def setup_project(project):
    template_folder = os.path.join(
        settings.BASE_DIR, 'projects', project.type, 'templates'
    )

    try:
        shutil.copytree(template_folder, project.project_folder)
    except shutil.Error:
        pass