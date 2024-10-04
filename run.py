from app import create_app, socketio
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    socketio.run(app, host=host, port=port, debug=True)