import { getRunCommand } from "./editor.js";

export const terminal = new Terminal();
const fitAddon = new FitAddon.FitAddon();

let terminalSocket = null;
let terminalUrl = null;
let attachAddon = null;
let firstRunCommand = false;
let firstReconnect = true;

terminal.open(document.getElementById("terminalApp"))
terminal.loadAddon(fitAddon);

window.onresize = event => {
    fitAddon.fit();
}

const showTerminalMessage = message => {
    $("#terminalMessage").text(message);
}

const hideTerminalMessage = () => {
    $("#terminalMessage").text("");
}

const terminalSocketOpen = e => {
    firstReconnect = true;
    hideTerminalMessage();
    attachAddon = new AttachAddon.AttachAddon(terminalSocket);
    terminal.loadAddon(attachAddon);

    const runCommand = getRunCommand();

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

export const attachTerminal = json_data => {
    terminalUrl = `ws://${json_data["terminal_address"]}?logs=0&stream=1&stdin=1&stdout=1&stderr=1`;
    terminalSocketWait();
}