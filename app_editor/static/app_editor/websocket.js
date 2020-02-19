import { READY, EXPLORER_UPDATE, RUN_SERVER, FILE_OPEN, FILE_CREATE, FOLDER_CREATE } from './consts.js';
import { explorerUpdate } from './explorer.js';
import { attachTerminal, openFile, renameNewFile } from './actions.js';
import { serverRunUpdate } from './events.js';


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
        } else if(data_type === RUN_SERVER) {
            serverRunUpdate(json_data);
            attachTerminal(json_data);
        } else if(data_type === FILE_OPEN) {
            openFile(json_data);
        } else if(data_type === FILE_CREATE || data_type === FOLDER_CREATE) {
            renameNewFile(json_data);
        }
    };

    editorSocket.onclose = e => {
        console.error("Editor socket closed unexpectedly");
    }
}

export const initTerminalSocket = () => {

}