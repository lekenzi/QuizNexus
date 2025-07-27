from email import message
import socket
from flask_socketio import SocketIO
import threading
from flask import request
from app.config import Config

from app.middleware.auth_middleware import jwt_auth_required, role_required

socketio = SocketIO(cors_allowed_origins="http://localhost:8080",message_queue=Config.REDIS_URL)
user_stop_events = {}  # Dictionary to store stop events for each user

@jwt_auth_required
@role_required(["user"])
@socketio.on("startquiz")
def handle_start_quiz():
    sid = request.sid  # Get the unique session ID for the user
    print(f"Session ID: {sid}")
    
    # Retrieve the JWT token from the request headers
    token = request.headers.get("Authorization")
    if token:
        print(f"Received JWT token: {token}")
    else:
        print("No JWT token provided")
    
    print("Quiz started")
    
    # Create a stop event for this user
    user_stop_events[sid] = threading.Event()
    stop_event = user_stop_events[sid]
    stop_event.clear()
    
    for countdown in range(100, 0, -1):
        if stop_event.is_set():
            print(f"Quiz stopped for user {sid}")
            break  
        print(f"Countdown for user {sid}: {countdown}")
        socketio.emit("countdown", {"count": countdown}, to=sid)
        socketio.sleep(1)

    # Clean up the stop event after the quiz ends
    user_stop_events.pop(sid, None)

@socketio.on("endquiz")
def handle_end_quiz():
    sid = request.sid  # Get the unique session ID for the user
    stop_event = user_stop_events.get(sid)
    if stop_event:
        stop_event.set()  # Stop the quiz for this user
        print(f"Quiz ended for user {sid}")

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid  # Get the unique session ID for the user
    stop_event = user_stop_events.get(sid)
    if stop_event:
        stop_event.set()  # Stop the quiz for this user
        print(f"Client {sid} disconnected")
    # Clean up the stop event
    user_stop_events.pop(sid, None)