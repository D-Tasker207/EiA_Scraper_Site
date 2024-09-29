from flask import Flask
from flask_socketio import SocketIO

socketIO = SocketIO()

def create_app():
    app =  app = Flask(__name__, static_folder='../static', static_url_path='/static')
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketIO.init_app(app)

    return app
