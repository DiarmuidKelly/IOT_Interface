# importing pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
import json
import threading

app = Flask(__name__)

logs = []

@app.route('/', methods=['GET'])
def receive_data():
    print(request.get_json())
    return json.dumps({'success' : True}), 200


@app.route('/ping', methods=['GET'])
def receive_data():
    print(request.get_json())
    return json.dumps({'ping' : 'pong}), 200

@app.route('/status', methods=['GET'])
def receive_data():
    print(request.get_json())
    return json.dumps({'ping' : 'pong}), 200
                       
                       
def setup_mongo():
    # establing connection
    try:
        connect = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.demoDB

    # creating or switching to demoCollection
    collection = db.sensor_readings


if __name__ == "__main__":
    app.run(host="192.168.178.23", port=3030)
