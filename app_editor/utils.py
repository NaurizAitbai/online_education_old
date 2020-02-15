import os
import shutil

from django.conf import settings

from app_projects.models import Project


def create_project_folder(project):
    project.project_identifier = 'pr-{}-{}'.format(project.id, project.name[:10])

    project_folder = os.path.join(
        settings.BASE_DIR,
        'uploads',
        'projects',
        '{}-{}'.format(project.user.username[:15], project.user.id),
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
    except FileExistsError:
        pass


def _get_files_from_directory(json_tree, fullpath, parent, base):
    for project_file in os.listdir(fullpath):
        file_fullpath = os.path.join(fullpath, project_file)
        file_path = os.path.relpath(file_fullpath, base)
        if os.path.isfile(file_fullpath):
            inode = os.stat(file_fullpath).st_ino
            json_tree.append({
                'id': 'file_{}'.format(inode),
                'parent': parent,
                'text': project_file,
                'type': 'file',
                'li_attr': {
                    'data-path': file_path
                }
            })
        elif os.path.isdir(file_fullpath):
            inode = os.stat(file_fullpath).st_ino
            file_id = 'file_{}'.format(inode)
            json_tree.append({
                'id': file_id,
                'parent': parent,
                'text': project_file,
                'type': 'folder',
                'li_attr': {
                    'data-path': file_path
                }
            })
            _get_files_from_directory(json_tree, file_fullpath, file_id, base)


def get_project_files_tree(project_id):
    """
    Получить список каталогов и файлов проекта
    """

    project = Project.objects.get(id=project_id)

    json_tree = [
        {
            'id': 'root',
            'parent': '#',
            'text': project.name,
            'type': 'folder',
            'state': {
                'opened': True
            },
        }
    ]

    _get_files_from_directory(
        json_tree, project.project_folder, 'root', project.project_folder
    )

    return json_tree