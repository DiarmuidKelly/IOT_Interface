import json

from flask import Flask, jsonify, request

from logger import Logger

app = Flask(__name__)

logger = None


@app.route('/', methods=['GET'])
def receive_data():
    logger.info("/")
    return json.dumps({'success': True}), 200


@app.route('/ping', methods=['GET'])
def ping():
    logger.info("/ping")
    return json.dumps({'ping': 'pong'}), 200


@app.route('/status', methods=['GET'])
def status():
    logger.info("/status", request.remote_addr)
    return jsonify(logger.print_logs()), 200


@app.route('/log-data', methods=['POST'])
def log_data():
    print()


if __name__ == "__main__":
    logger = Logger()
    app.run(host="0.0.0.0", port=3030)
