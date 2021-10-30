import json

from flask import Flask, jsonify, request

from logger import Logger
from db.sqllite_dbdriver import SQLLiteDBDriver

app = Flask(__name__)

logger = None


@app.route('/', methods=['GET'])
def receive_data():
    logger.info("/", request.remote_addr)
    dat = database_driver.get_records("data")
    return jsonify(dat), 200


@app.route('/ping', methods=['GET'])
def ping():
    logger.info("/ping", request.remote_addr)
    database_driver.get_records("data")
    return json.dumps({'ping': 'pong'}), 200


@app.route('/status', methods=['GET'])
def status():
    logger.info("/status", request.remote_addr)
    return jsonify(logger.print_logs()), 200


@app.route('/log-data', methods=['POST'])
def log_data():
    logger.info("/log-data", request.remote_addr)
    data = request.json
    database_driver.add_record("data", data, request.remote_addr, "INFO")
    return json.dumps({'success': True}), 200


if __name__ == "__main__":
    database_driver = SQLLiteDBDriver(5, path_to_db="./data")
    logger = Logger(database_driver, 5)
    database_driver.setup_table("data", "data text, caller text, log_level text")

    app.run(host="0.0.0.0", port=3030)
