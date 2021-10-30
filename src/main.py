import json

from flask import Flask, jsonify, request

from logger import Logger
from db.sqllite_dbdriver import SQLLiteDBDriver
from configparser import ConfigParser
app = Flask(__name__)

logger = None
config = ConfigParser()
config.read('config.ini')
config = config['DEFAULT']


@app.route('/', methods=['GET'])
def receive_data():
    logger.info(str(request), request.remote_addr)
    dat = database_driver.get_records("data")
    return jsonify(dat), 200


@app.route('/ping', methods=['GET'])
def ping():
    logger.info(str(request), request.remote_addr)
    database_driver.get_records("data")
    return json.dumps({'ping': 'pong'}), 200


@app.route('/status', methods=['GET'])
def status():
    logger.info(str(request), request.remote_addr)
    return jsonify(logger.print_logs()), 200


@app.route('/log-data', methods=['POST'])
def log_data():
    logger.info([str(request), str(request.data)], request.remote_addr)
    data = request.json
    database_driver.add_record("data", data, request.remote_addr, "INFO", queue_length)
    return json.dumps({'success': True}), 200


if __name__ == "__main__":
    database_driver = SQLLiteDBDriver(path_to_db=config['database_directory'], persistence=config['persistent_database'])
    logger = Logger(database_driver, queue_length=int(config['log_queue_length']))
    queue_length = int(config['data_queue_length'])
    database_driver.setup_table(table_name="data", keys="data text, caller text, log_level text")

    logger.info("Starting up", "host")

    app.run(host=config['host'], port=int(config['port']))
