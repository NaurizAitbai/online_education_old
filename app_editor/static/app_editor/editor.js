import { editorSocket, initEditorSocket, initTerminalSocket } from './websocket.js';
import { initExplorer } from './explorer.js';
import { saveFile, createFile, runServer, runFile } from './actions.js';


let runCommand = null;
let runFileCommand = null;
let currentFile = null;
export let openedFiles = {};

export const getRunCommand = () => {
    return runCommand;
}

export const setRunCommand = newRunCommand => {
    runCommand = newRunCommand;
}

export const getRunFileCommand = () => {
    return runFileCommand;
}

export const setRunFileCommand = newRunFileCommand => {
    runFileCommand = newRunFileCommand;
}

export const getCurrentFile = () => {
    return currentFile;
}

export const setCurrentFile = newFile => {
    currentFile = newFile;
}

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