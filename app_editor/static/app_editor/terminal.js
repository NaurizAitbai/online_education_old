import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { AttachAddon } from "xterm-addon-attach";

const terminal = new Terminal();
const fitAddon = new FitAddon();

let terminalSocket = null;
let terminalUrl = null;
let attachAddon = null;
let firstRunCommand = false;
let firstReconnect = true;

terminal.open(document.getElementById("terminal_app"))
terminal.loadAddon(fitAddon);

window.onresize = event => {
    fitAddon.fit();
}

const showTerminalMessage = message => {
    $("#terminal_message").text(message);
}

const hideTerminalMessage = () => {
    $("#terminal_message").text("");
}

const terminalSocketOpen = e => {
    firstReconnect = true;
    hideTerminalMessage();
    attachAddon = new AttachAddon(terminalSocket);
    terminal.loadAddon(attachAddon);
    if(!firstRunCommand) {
        terminal.paste("\n");
        if(runCommand) {
            terminal.paste(runCommand + "\n");
        }
        firstRunCommand = true;
    }
};

const terminalSocketClose = e => {
    if (firstReconnect) {
        firstReconnect = false;
        terminalReconnect();
    } else {
        showTerminalMessage("Повторное подключение");
        terminalSocketWait();
    }
};

const terminalSocketWait = () => {
    setTimeout(() => {
        terminalReconnect();
    }, 1000);
};

const terminalReconnect = () => {
    terminalSocket = new WebSocket(terminalUrl);
    terminalSocket.onopen = terminalSocketOpen;
    terminalSocket.onclose = terminalSocketClose;
};

const attach_terminal = json_data => {
    terminalUrl = `ws://${json_data["terminal_address"]}?logs=0&stream=1&stdin=1&stdout=1&stderr=1`;
    terminalSocketWait();
}