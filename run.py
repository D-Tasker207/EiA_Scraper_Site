from app import create_app, socketIO
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    socketIO.run(app, host=host, port=port, debug=True)