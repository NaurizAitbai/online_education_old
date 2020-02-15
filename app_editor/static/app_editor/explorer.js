import { createFile, createFolder } from './actions.js';


export const initExplorer = () => {
    $("#explorer").jstree({
        core: {
            check_callback: true
        },
        types: {
            folder: {
                icon: "far fa-folder",
                valid_children: ["folder", "file"]
            },
            file: {
                icon: "far fa-file-alt",
                valid_children: []
            }
        },
        sort: function(a, b) {
            a_node = this.get_node(a);
            b_node = this.get_node(b);
            if (a_node.type == b_node.type) {
                return a_node.text > b_node.text ? 1 : -1;
            } else {
                return a_node.type < b_node.type ? 1 : -1;
            }
        },
        contextmenu: {
            items: function($node) {
                return {
                    createFile: {
                        label: labels.CREATE_FILE,
                        action: obj => {
                            createFile();
                        }
                    },
                    createFolder: {
                        label: labels.CREATE_FOLDER,
                        action: obj => {
                            createFolder();
                        }
                    }
                }
            }
        },
        plugins: ["types", "contextmenu", "dnd", "sort", "state", "unique"]
    })
}

/**
 * Получает список файлов проекта с сервера и обновляет проводник проекта
 * @param {string} json_data Данные полученные с WebSocket
 */
export const explorerUpdate = json_data => {
    const project_files_tree = json_data['project_files_tree'];

    $("#explorer").jstree(true).settings.core.data = project_files_tree;
    $("#explorer").jstree(true).refresh();
};