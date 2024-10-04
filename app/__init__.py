from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO(async_mode="threading")

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    socketio.init_app(app, cors_allowed_origins="http://localhost:3000")

    return app
