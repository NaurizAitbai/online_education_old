import json

from channels.generic.websocket import WebsocketConsumer
from .consts import SOCKET_TYPES, STATUS
from .utils import get_project_files_tree


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