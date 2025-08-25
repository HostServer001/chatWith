import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, send
import os
import eventlet
eventlet.monkey_patch()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    logging.info(f"Message: {msg}")
    send(msg, broadcast=True)

@socketio.on('join')
def handle_join(nickname):
    logging.info(f"{nickname} joined the chat")
    send(f"{nickname} has entered the chat", broadcast=True)

@socketio.on('chat_message')
def handle_chat(data):
    nickname = data['nickname']
    msg = data['msg']
    send(f"{nickname}: {msg}", broadcast=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
