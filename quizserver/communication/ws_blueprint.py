from flask import Blueprint
from flask_socketio import emit

from data import LobbyData, lobbies

ws_blueprint = Blueprint('ws_blueprint', __name__)


# Websocket events:
# Incoming:
# - Connect to lobby
# - Disconnect
# Outgoing:
# - New User in lobby
# - User disconnected
# - New Question
# - New Answer (To admin UUID only)

# @socketio.on('connect')
def connect():
    print('Client connected')
