import io from 'socket.io-client';

let socket;

export const connectSocket = (setProgress, setMessage, setError, setDownloadLink) => {
    return new Promise((resolve, reject) => {
        if(socket && socket.connected) {
            resolve(socket.id);
        } else {
            socket = io();

            socket.on('connect', () => {
                console.log('Websocket connected, socket id:', socket.id);
                
                socket.on('progress', (data) => {
                    // console.log('Progress:', data);
                    if(setProgress) {
                        setProgress(data);
                    }
                });

                socket.on('error', (data) => {
                    // console.log('Error:', data);
                    if(setError) {
                        setMessage(data);
                    }
                });
            
                socket.on('message', (data) => {
                    // console.log('Message:', data);
                    if(setMessage) {
                        setMessage(data);
                    }
                });

                socket.on('url', (data) => {
                    // console.log('Download Link:', data);
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