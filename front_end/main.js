const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    // Load the HTML file
    mainWindow.loadFile(path.join(__dirname, 'index.html'));

    // Read queue time from the JSON file created by Python
    const queueTimeFilePath = path.join(__dirname, 'queue_time.json');
    const queueTimeData = fs.readFileSync(queueTimeFilePath, 'utf-8');
    const queueTime = JSON.parse(queueTimeData).queue_time;

    // Send the queue time to the frontend
    mainWindow.webContents.send('queue-time', queueTime);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
