from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # Use SocketIO with gevent for WebSocket support
    socketio.run(app, debug=True, host='0.0.0.0', port=8080) 