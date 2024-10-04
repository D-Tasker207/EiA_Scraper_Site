from flask_socketio import emit, disconnect
from . import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def client_disconnect(sid):
    socketio.server.disconnect(sid)

def send_progress(sid, progress):
    socketio.emit('progress', progress, room=sid)

def send_message(sid, message):
    socketio.emit('message', message, room=sid)

def send_error(sid, error):
    socketio.emit('error', error, room=sid)

def send_url(sid, url):
    socketio.emit('url', url, room=sid)

class Progress:
    def __init__(self, sid, total_steps):
        self.sid = sid
        self.total_steps = total_steps
        self.current_step = 0

    def update(self, message):
        send_message(self.sid, message)
        self.current_step += 1
        send_progress(self.sid, round(self.current_step / self.total_steps * 100))