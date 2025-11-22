# backend/app.py
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Config
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

# THIS IS THE FIX → Remove async_mode="eventlet"
socketio = SocketIO(
    app,
    cors_allowed_origins="*"
    # Works perfectly with default 'threading' mode on Windows
)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['VOICE_FOLDER'], exist_ok=True)

from models import init_db
with app.app_context():
    init_db()
    logger.info("Database tables ready")

# Register blueprints
from routes.auth import auth_bp
# from routes.prescription import prescription_bp
# from routes.reminders import reminders_bp
# from routes.history import history_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
# app.register_blueprint(prescription_bp, url_prefix='/api/prescription')
# app.register_blueprint(reminders_bp, url_prefix='/api/reminders')
# app.register_blueprint(history_bp, url_prefix='/api/history')

# Socket events
from sockets.events import register_socket_events
register_socket_events(socketio)

@app.route('/')
def health():
    return {"status": "API Running", "socketio": "threading mode"}

if __name__ == '__main__':
    logger.info("Starting server on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)