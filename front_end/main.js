const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false // Allow communication between Electron and frontend
        }
    });

    mainWindow.loadFile(path.join(__dirname, 'index.html'));

    // Function to send queue time to frontend
    function sendQueueTime() {
        const queueTimeFilePath = path.join(__dirname, 'queue_time.json');

        if (fs.existsSync(queueTimeFilePath)) {
            try {
                const queueTimeData = fs.readFileSync(queueTimeFilePath, 'utf-8');
                const queueTime = JSON.parse(queueTimeData).queue_time;

                console.log("Updating queue time:", queueTime);
                mainWindow.webContents.send('queue-time', queueTime);
            } catch (error) {
                console.error("Error reading queue time file:", error);
            }
        } else {
            console.error("Queue time file not found:", queueTimeFilePath);
        }
    }

    // Watch the file for changes and update the frontend
    const queueTimeFilePath = path.join(__dirname, 'queue_time.json');
    fs.watch(queueTimeFilePath, (eventType) => {
        if (eventType === 'change') {
            sendQueueTime();
        }
    });

    // Send the initial queue time when the window loads
    mainWindow.webContents.once('did-finish-load', sendQueueTime);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
