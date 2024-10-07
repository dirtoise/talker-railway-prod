from app import create_app, socketio
from config import DevConfig, ProdConfig
import os

if __name__ == '__main__':
    app = create_app(ProdConfig)
    socketio.run(app, port=os.getenv("PORT", default=5000))
