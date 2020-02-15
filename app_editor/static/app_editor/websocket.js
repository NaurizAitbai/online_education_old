import { READY, EXPLORER_UPDATE } from './consts.js';
import { explorerUpdate } from './explorer.js';


export var editorSocket = null;

export const initEditorSocket = () => {
    editorSocket = new WebSocket(
        "ws://" + window.location.host + "/ws/project/" + project.id + "/"
    );

    editorSocket.onopen = e => {
        editorSocket.send(
            JSON.stringify({
                type: READY,
                user: user.id,
                project: project.id
            })
        );
    };

    editorSocket.onmessage = e => {
        const json_data = JSON.parse(e.data);

        const data_type = json_data['type'];

        if (data_type === EXPLORER_UPDATE) {
            explorerUpdate(json_data);
        }
    }

    editorSocket.onclose = e => {
        console.error("Editor socket closed unexpectedly");
    }
}