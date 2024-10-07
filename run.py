from app import create_app, socketio
from config import DevConfig, ProdConfig
import os

if __name__ == '__main__':
    app = create_app(DevConfig)
    socketio.run(app, host="0.0.0.0", port=os.getenv("PORT", default=5000))
