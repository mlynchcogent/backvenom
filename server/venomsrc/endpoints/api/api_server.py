from flask import Flask, jsonify, request, Response
from venomsrc.config import Config
from functools import wraps
from flask import abort

import venomsrc.listener.TCP

from venomsrc.listener.exceptions import *

app = Flask("BackVenom")
CONFIG = Config()



def login_required(f):
    """
    API passwd required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("password") != Config.getPass():
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index() -> str:
    return 'BackVenom API'

@app.route('/start/listener/<option>', methods=['POST'])
@login_required
def listener(option: str) -> str:  # TODO: Return?
    data = request.form

    if option == "tcp":
        if not "lport" in data:
            return jsonify("port necessary")

        if not "payload" in data:
            return jsonify("Specify payload")

        if not "lhost" in data:
            return jsonify("Specify lhost")

        try:
            tcp_handle = venomsrc.listener.TCP.TCPListener(data["lhost"], data["lport"], data["payload"])
            tcp_handle.init()   
        except ListenerAlredyStarted:
            return jsonify("Listener alredy started")
        except InvalidPayload:
            return jsonify("Not a valid payload")
        except InvalidPort:
            return jsonify("Not a valid port")

        return jsonify("Started TCP Listener")

    return "Listener " + option + " not found", 404
def start_api() -> None:
    """
    Start Flask server
    """
    context = (CONFIG.CERT_FILE, CONFIG.KEY_FILE)  # certificate and key files for API
    app.run(debug=True, ssl_context=context)

if __name__=="__main__":
    start_api()