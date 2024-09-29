from app import create_app, socketio
from config import DevConfig

if __name__ == '__main__':
    app = create_app(DevConfig)
    socketio.run(app)