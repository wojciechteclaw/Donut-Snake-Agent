import json
import logging
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jEbacPiS1312312412412'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
socketio.threaded = True
app.debug = False

logging.basicConfig(filename='server.log', level=logging.ERROR)

@app.route("/publish-environment", methods=["POST"])
def publish_food():
    request_data = request.data
    data = json.loads(request_data)
    socketio.emit('new_environment', data)
    return "OK"

@app.route("/health", methods=["GET"])
def health():
    return "OK"

if __name__ == "__main__":
    socketio.run(app,
                 host='0.0.0.0',
                 port=5001,
                 use_reloader=False,
                 debug=False,
                 log_output=True,
                 allow_unsafe_werkzeug=True)