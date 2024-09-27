from flask_socketio import emit
from . import socketIO

def send_progress(sid, progress):
    emit('progress', {'progress': progress}, to=sid)

def send_message(sid, message):
    emit('message', {'message': message}, to=sid)

def send_error(sid, error):
    emit('error', {'error': error}, to=sid)

def send_redirect(sid, url):
    emit('redirect', {'url': url}, to=sid)