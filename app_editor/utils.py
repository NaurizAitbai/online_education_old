import os
import docker
import shutil

from django.conf import settings
from django.contrib.auth.models import User

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


def run_container(client, project):
    project_type = project.type

    if project_type == 'simple_web':
        container = client.containers.run('simple_web', command='/bin/bash', detach=True, stdin_open=True, tty=True,
                        volumes={
                            project.project_folder: {
                                'bind': '/usr/share/nginx/html', 'mode': 'rw'
                            }
                        })
        port = 80
        run_command = 'service nginx start'
        run_file = None
    elif project_type == 'reactjs_web':
        container = client.containers.run('reactjs_web', command='/bin/sh', detach=True, stdin_open=True, tty=True,
                        volumes={
                            '{}:/app'.format(project.project_folder),
                            '/app/node_modules'
                        })
        port = 3000
        run_command = 'cd /app && npm start'
        run_file = None
    elif project_type == 'simple_python':
        container = client.containers.run('simple_python', command='/bin/bash', detach=True, stdin_open=True, tty=True,
                        volumes={
                            '{}:/app'.format(project.project_folder)
                        })
        port = 80
        run_command = None
        run_file = 'cd /app && python3 :FILE_NAME:'
    elif project_type == 'django_python':
        container = client.containers.run('django_python', command='/bin/bash', detach=True, stdin_open=True, tty=True,
                        volumes={
                            '{}:/app'.format(project.project_folder)
                        }
        port = 8000
        run_command = 'cd /app && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000'
        run_file = None
    elif project_type == 'pygame_python':
        container = client.containers.run('pygame_python', entrypoint='/bin/bash', detach=True, stdin_open=True, tty=True,
                        volumes={
                            '{}:/app'.format(project.project_folder),
                            '/dev/shm:/dev/shm'
                        })
        port = None
        run_command = 'nohup /startup.sh &'
        run_file = 'cd /app && python3 :FILE_NAME:'
    elif project_type == 'simple_php':
        container = client.containers.run('simple_php', command='/bin/bash', detach=True, stdin_open=True, tty=True,
                        volumes=[
                            '{}:/var/www/html'.format(project.project_folder),
                        ])
        port = 80
        run_command = './bin/run_server.sh'
        run_file = None
    elif project_type == 'wordpress_php':
        container = client.containers.run('wordpress_php', command='/bin/bash', detach=True, stdin_open=True, tty=True,
                        volumes=[
                            '{}:/var/www/html'.format(project.project_folder),
                        ])
        port = 80
        run_command = './bin/run_server.sh'
        run_file = None
    return container, port, run_command, run_file


def run_server(project_id):
    project = Project.objects.get(id=project_id)

    docker_host = settings.DOCKER_HOST
    docker_port = settings.DOCKER_PORT

    client = docker.DockerClient(
        base_url='tcp://{}:{}'.format(docker_host, docker_port))
    )

    container, port, run_command, run_file = run_container(client, project)
    container.reload()
    ip = container.attrs['NetworkSettings']['IPAddress']
    container_id = container.id
    conf_path = os.path.join(
        os.sep,
        'etc',
        'nginx',
        'apps',
        project.project_identifier
    )

    conf_file = open(conf_path, 'w')
    conf_file.write(
        """
        server {{
            server_name {0}.{3}
            listen 80;

            location / {{
                include proxy_params;
                proxy_pass http://{1};
            }}

            location /websockify {{
                include proxy_params;
                proxy_pass http://{1}/websockify;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_ugprade;
                proxy_set_header Connection "upgrade";
            }}

            location /{2} {{
                include proxy_params;
                proxy_pass http://{4}:{5}/containers/{2}/attach/ws;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
            }}
        }}
        """.format(project.project_identifier, ip + (':' + str(port) if port else ''), container_id, settings.DOCKER_BASE_DOMAIN, docker_host, docker_port)
    )

    os.popen("sudo systemctl reload nginx.service")

    return container, "{}.{}".format(project.project_identifier, settings.DOCKER_BASE_DOMAIN), "{}.{}/{}".format(project.project_identifier, settings.DOCKER_BASE_DOMAIN, container_id), run_command, run_file


    def get_file_content(project_id, file_path):
        project =  Project.objects.get(id=project_id)

        file_fullpath = os.path.join(project.project_folder, file_path)

        fd = open(file_fullpath, 'r')
        file_content = fd.read()
        fd.close()

        return file_content
    

    def set_file_content(project_id, filename, content):
        project = Project.objects.get(id=project_id)

        file_path = os.path.join(project.project_folder, filename)

        fd = open(file_path, 'w')
        fd.write(content)
        fd.close()
    

    def create_file(project_id, filename, parent_path):
        project = Project.objects.get(id=project_id)

        file_path = os.path.join(project.project_folder, parent_path, filename)

        open(file_path, 'a').close()

        inode = os.stat(file_path).st_ino

        return inode
    

    def create_folder(project_id, filename, parent_path):
        project = Project.objects.get(id=project_id)

        file_path = os.path.join(project.project_folder, parent_path, filename)

        os.mkdir(file_path)

        inode = os.stat(file_path).st_ino

        return inode