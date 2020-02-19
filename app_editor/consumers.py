import json

from channels.generic.websocket import WebsocketConsumer
from .consts import SOCKET_TYPES, STATUS
from .utils import get_project_files_tree, get_file_content, set_file_content, create_file, create_folder


class EditorConsumer(WebsocketConsumer):
    def connect(self):
        self.docker = None
        self.accept()

    def disconnect(self, close_node):
        if self.docker:
            self.docker.stop()

    def receive(self, text_data):
        data = json.loads(text_data)

        type = data['type']
        project_id = data['project']

        if type == SOCKET_TYPES.READY:
            project_files_tree = get_project_files_tree(project_id)

            self.send(
                text_data=json.dumps({
                    'type': SOCKET_TYPES.EXPLORER_UPDATE,
                    'status': STATUS.SUCCESS,
                    'project_files_tree': project_files_tree
                })
            )
        elif type == SOCKET_TYPES.RUN_SERVER:
            if not self.docker:
                self.docker, address, terminal_address, run_command, run_file = run_server(project_id)

            self.send(
                text_data=json.dumps({
                    'type': SOCKET_TYPES.RUN_SERVER,
                    'status': STATUS.SUCCESS,
                    'address': address,
                    'terminal_address': terminal_address,
                    'run_command': run_command,
                    'run_file': run_file
                })
            )
        elif type == SOCKET_TYPES.FILE_OPEN:
            file_path = data['file']
            tree_id = data['tree_id']
            file_content = get_file_contentproject_id, file_path)

            self.send(
                text_data=json.dumps({
                    'type': SOCKET_TYPES.FILE_OPEN,
                    'status': STATUS.SUCCESS,
                    'tree_id': tree_id,
                    'path': file_path,
                    'content': file_content
                })
            )
        elif type == SOCKET_TYPES.FILE_SAVE:
            file_path = data['file']
            file_content = data['content']
            set_file_content(project_id, file_path, file_content)

            self.send(
                text_data=json.dumps({
                    'type': SOCKET_TYPES.FILE_SAVE,
                    'status': STATUS.SUCCESS,
                    'path': file_path
                })
            )
        elif type == SOCKET_TYPES.FILE_CREATE:
            file_path = data['file']
            if 'parent_path' in data:
                parent_path = data['parent_path']
            else:
                parent_path = ''

            path = os.path.join(parent_path, file_path)
            inode = create_file(project_id, file_path, parent_path)

            self.send(
                text_data=json.dumps({
                    'type': SOCKET_TYPES.FILE_CREATE,
                    'status': STATUS.SUCCESS,
                    'path': path,
                    'inode': inode
                })
            )
        elif type == SOCKET_TYPES.FOLDER_CREATE:
            file_path = data['file']
            if 'parent_path' in data:
                parent_path = data['parent_path']
            else:
                parent_path = ''
            
            path = os.path.join(parent_path, file_path)
            inode = create_folder(project_id, file_path, parent_path)

            self.send(
                text_data=json.dumps({
                    'type': SOCKET_TYPES.FOLDER_CREATE,
                    'status': STATUS.SUCCESS,
                    'path': path,
                    'inode': inode
                })
            )