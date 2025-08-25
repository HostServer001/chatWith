import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
from datetime import datetime
import eventlet
eventlet.monkey_patch()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve the chat page
@app.route('/')
def index():
    return render_template('index.html')  # Make sure index.html exists in the 'templates' folder

# Handle generic messages
@socketio.on('message')
def handle_message(msg):
    emit('message', msg, broadcast=True)

# Handle user joining
@socketio.on('join')
def handle_join(nickname):
    logging.info(f"{nickname} joined the chat")
    
    # Broadcast join message to everyone
    join_msg = f"{nickname} has entered the chat"
    emit('message', join_msg, broadcast=True)
    
    # Read previous chat history
    file_path = os.path.join(app.root_path, "chat.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            history = file.readlines()
        
        # Send chat history only to the joining user
        for line in history:
            emit('message', line.strip())

# Handle chat messages
@socketio.on('chat_message')
def handle_chat(data):
    nickname = data.get('nickname', 'Anonymous')
    msg = data.get('msg', '')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = f"[{timestamp}] {nickname}: {msg}"

    # Broadcast to all clients
    emit('message', output, broadcast=True)

    # Append to chat.txt
    file_path = os.path.join(app.root_path, "chat.txt")
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(output + "\n")

    # Log to console
    logging.info(output)

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
