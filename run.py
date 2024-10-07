from app import create_app, socketio
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == '__main__':
    host = "0.0.0.0"
    if os.environ.get('FLASK_ENV') == 'development':
        host = "127.0.0.1"
    
    socketio.run(app, host=host, port=5000, debug=True)