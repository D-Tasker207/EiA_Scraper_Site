from app import create_app, socketIO

app = create_app()

if __name__ == '__main__':
    socketIO.run(app, host='0.0.0.0', port=5000)