import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO(async_mode="threading")

def create_app():
    app = Flask(__name__)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    if os.environ.get('FLASK_ENV') == 'development':
        app.config['DEBUG'] = True
        app.config['ENV'] = 'development'
        CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
        socketio.init_app(app, cors_allowed_origins="http://localhost:3000")
    else:
        app.config['DEBUG'] = False
        app.config['ENV'] = 'production'
        socketio.init_app(app)

    return app