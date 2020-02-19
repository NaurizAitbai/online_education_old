import { editorSocket, initEditorSocket, initTerminalSocket } from './websocket.js';
import { initExplorer } from './explorer.js';
import { saveFile, createFile, runServer } from './actions.js';


let runCommand = null;
let runFileCommand = null;
let currentFile = null;
let openedFiles = {};

// Инициализировать проводник редактора
initExplorer();

// Инициализировать websocket редактора
initEditorSocket();
initTerminalSocket();


$("#saveFileButton").click(() => {
    saveFile();
})

$("#newFileButton").click(() => {
    createFile();
})

$("#runButton").click(() => {
    runServer();
})

$("#runFileButton").click(() => {
    runFile();
})