from app import create_app, socketio
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()
if os.environ.get('FLASK_ENV') == 'development':
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)