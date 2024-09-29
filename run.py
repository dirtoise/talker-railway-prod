from app import create_app, socketio
from config import DevConfig, ProdConfig

if __name__ == '__main__':
    app = create_app(ProdConfig)
    socketio.run(app)
