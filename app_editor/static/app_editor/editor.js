import { editorSocket, initEditorSocket } from './websocket.js';
import { initExplorer } from './explorer.js';


// Инициализировать проводник редактора
initExplorer();

// Инициализировать websocket редактора
initEditorSocket();