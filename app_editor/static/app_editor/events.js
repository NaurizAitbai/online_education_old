import { SUCCESS } from './consts.js';
import { setRunCommand, setRunFileCommand } from './editor.js';


/**
 * Обновляет состояние интерфейса, если сервер успешно запущен
 * @param {string} json_data Данные полученные с WebSocket
 */
export const serverRunUpdate = (json_data) => {
    const status = json_data['status'];

    if(status == SUCCESS) {
        const address = json_data["address"];
        $("#runButton").attr('disabled', 'disabled');
        $("#serverAddressLabel").html(`<a href="http://${address}">${address}</a>`);
        setRunCommand(json_data['run_command']);
        setRunFileCommand(json_data['run_file']);
    }
};