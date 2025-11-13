from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # Allow frontend to connect
socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure upload folders exist
import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['VOICE_FOLDER'], exist_ok=True)

# Register routes & sockets later
from routes import *
from sockets.events import *

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)