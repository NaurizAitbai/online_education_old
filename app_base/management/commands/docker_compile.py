import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

PROJECTS = [
    'simple_web',
    'simple_php',
    'simple_python',
    'reactjs_web',
    'wordpress_php',
    'django_python',
    'pygame_python',
]

class Command(BaseCommand):
    help = 'Компилирует Docker-образы'

    def handle(self, *args, **options):
        for project in PROJECTS:
            os.system("cd {}/projects/{}/docker && chmod +x compile && ./compile {} {}".format(settings.BASE_DIR, project, settings.DOCKER_HOST, settings.DOCKER_PORT))