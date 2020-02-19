import { SUCCESS, FILE_SAVE, FOLDER, FILE_CREATE, FOLDER_CREATE, RUN_SERVER } from './consts.js';

import { editorSocket } from './websocket.js';

/**
 * Создает новый файл.
 */
export const createFile = () => {
    const selectedNodes = $("#explorer").jstree("get_selected", true);
    let parentId = null;

    if(selectedNodes.length == 1) {
        const selectedNode = selectedNodes[0];

        if (selectedNode.type === FOLDER) {
            parentId = selectedNode.id;
        } else {
            parentId = selectedNode.parent;
        }
    } else if (selectedNodes.length == 0) {
        parentId = "root";
    } else {
        return;
    }

    const node = $("#explorer").jstree(true).create_node(parentId, { id: "new", type: "file", text: ""});
    $("#explorer").jstree(true).edit(node, null, function(node, status) {
        if (status === true) {
            const parentNode = $("#explorer").jstree(true).get_node(parent_id);

            editorSocket.send(JSON.stringify({
                type: FILE_CREATE,
                project: project.id,
                parent_path: parentNode.li_attr["data-path"],
                file: node.text
            }));
        } else {
            $("#explorer").jstree(true).delete_node(node);
        }
    });
};

/**
 * Создает новую папку.
 */
export const createFolder = () => {
    const selectedNodes = $("#explorer").jstree("get_selected", true);
    let parentId = null;

    if(selectedNodes.length == 1) {
        const selectedNode = selectedNodes[0];

        if (selectedNode.type === FOLDER) {
            parentId = selectedNode.id;
        } else {
            parentId = selectedNode.parent;
        }
    } else if (selectedNodes.length == 0) {
        parentId = "root";
    } else {
        return;
    }

    const node = $("#explorer").jstree(true).create_node(parentId, { id: "new", type: "folder", text: ""});
    $("#explorer").jstree(true).edit(node, null, function(node, status) {
        if (status === true) {
            const parentNode = $("#explorer").jstree(true).get_node(parent_id);

            editorSocket.send(JSON.stringify({
                type: FOLDER_CREATE,
                project: project.id,
                parent_path: parentNode.li_attr["data-path"],
                file: node.text
            }));
        } else {
            $("#explorer").jstree(true).delete_node(node);
        }
    });
}

/**
 * Отправляет запрос на запуск Docker-контейнера
 */
export const runServer = () => {
    editorSocket.send(JSON.stringify({
        type: RUN_SERVER,
        project: project.id
    }))
};

export const runFile = () => {
    if(runFileCommand) {
        const parsedRunFile = runFileCommand
            .replace(":FILE_NAME:", currentFile)
            .replace(":FILE_NAME_NO_EXT:", currentFile.split(".")[0]);
        $("#terminal").paste(parsedRunFile + "\n");
    }
};

export const attachTerminal = (json_data) => {

}

/**
 * Создает новую вкладку и редактор, и заполняет этот редактор данными из файла
 * @param {string} json_data Данные полученные с WebSocket
 */
export const openFile = (json_data) => {
    const filePath = json_data['path'];
    const fileContent = json_data['content'];
    const treeId = json_data['tree_id'];

    if($.isEmptyObject(openedFiles)) {
        $("#editorTab").append(
            `
            <li class="nav-item"><a id="tab_${treeId} class="nav-link active" data-toggle="tab" href="#pane_${treeId}" role="tab" aria-controls="pane_${treeId}" aria-selected="false">${filePath}</a></li>
            `
        );
        $("#editorPane").append(
            `
            <div id="pane_${treeId} class="tab-pane show active" role="tabpanel" aria-labelledby="tab_${treeId}">
                <textarea id="editor_${treeId}"></textarea>
            </div>
            `
        )
        currentFile = filePath;
    } else {
        $("#editorTab").append(
            `
            <li class="nav-item"><a id="tab_${treeId} class="nav-link" data-toggle="tab" href="#pane_${treeId}" role="tab" aria-controls="pane_${treeId}" aria-selected="false">${filePath}</a></li>
            `
        );
        $("#editorPane").append(
            `
            <div id="pane_${treeId} class="tab-pane" role="tabpanel" aria-labelledby="tab_${treeId}">
                <textarea id="editor_${treeId}"></textarea>
            </div>
            `
        )
    }
};


/**
 * Изменяет название новосозданного файла
 * @param {string} json_data Данные полученные с WebSocket
 */
export const renameNewFile = (json_data) => {
    const inode = json_data['inode'];
    const filePath = json_data['path'];
    const newNode = $("#explorer").jstree(true).get_node('new');
    $("#explorer").jstree(true).set_id(newNode, `file_${inode}`);
    newNode.li_attr['data-path'] = filePath;
}

/**
 * Сохраняет содержимое файла.
 */
export const saveFile = () => {
    editorSocket.send(JSON.stringify({
        type: FILE_SAVE,
        project: project.id,
        file: currentFile,
        content: openedFiles[currentFile]["editor"].getValue()
    }))
};