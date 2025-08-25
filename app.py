import os
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return "Chat server is running!"

@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    socketio.run(app, host='0.0.0.0', port=port)
