from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from communication.api_blueprint import api_blueprint
from communication.ws_blueprint import ws_blueprint
import data


app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(ws_blueprint)

socketio = SocketIO(app)
# Allow CORS for all domains on all routes. Probably scary... Let me drop a TODO here.
CORS(app)

if __name__ == '__main__':
    data.seed_data()
    app.run(debug=True)
    socketio.run(app, debug=True)
