from flask_socketio import send, emit
from .. import socketio


@socketio.on('ping')
def ping_reply(json):
    emit('pong', json)
