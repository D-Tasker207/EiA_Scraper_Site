import io from 'socket.io-client';

let socket;

export const connectSocket = (setProgress, setMessage, setDownloadLink) => {
    return new Promise((resolve, reject) => {
        if(socket && socket.connected) {
            resolve(socket.id);
        } else {
            socket = io('http://localhost:5000', { timeout: 5000 });

            socket.on('connect', () => {
                console.log('Websocket connected, socket id:', socket.id);
                
                socket.on('progress', (data) => {
                    console.log('Progress:', data);
                    if(setProgress) {
                        setProgress(data);
                    }
                });
            
                socket.on('message', (data) => {
                    console.log('Message:', data);
                    if(setMessage) {
                        setMessage(data);
                    }
                });

                socket.on('url', (data) => {
                    console.log('Download Link:', data);
                    if(setDownloadLink) {
                        setDownloadLink(data);
                    }
                });
            
                socket.on('disconnect', () => {
                    console.log('Websocket disconnected');
                });

                resolve(socket.id);
            });

            socket.on('connect_error', (err) => {
                console.log('Websocket connection error:', err);
                reject(err);
            });
        }
    });
};

export const sendMessage = (data) => {
    if(socket) {
        socket.emit('message', data);
    }
};

export const disconnectSocket = () => {
    if(socket) {
        socket.disconnect();
        socket = null;
    };
};

export const getSocketId = () => {
    if(socket) {
        return socket.id;
    }
    return null;
};