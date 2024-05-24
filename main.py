from flask import Flask, render_template, jsonify, request
import os
import subprocess
import requests
import sys
import time
import json
import uuid
from dotenv import dotenv_values
from adafruit_mqtt import Adafruit_MQTT
from Adafruit_IO import MQTTClient

env_config = dotenv_values('.env')

AIO_KEY = os.environ.get('IO_KEY')

AIO_FEED_IDs = ['iot-temperature','iot-humidity','iot-mobile']
AIO_USERNAME = 'nemo2602'
AIO_KEY = os.environ['IO_KEY'] if ('IO_KEY' in os.environ) else env_config['IO_KEY']

def callBackFunc_Message(feed_id, payload):
    print("Feed: " + feed_id + " - Value: " + payload)
    if feed_id == 'iot-temperature':
        data = read_data_from_json('data.json')
        data['temp'] = float(payload)
        write_data_to_json(data, 'data.json')

    if feed_id == 'iot-humidity':
        data = read_data_from_json('data.json')
        data['humi'] = float(payload)
        write_data_to_json(data, 'data.json')

# MAIN PROGRAM
# Create an instance of Adafruit_MQTT class
client = Adafruit_MQTT(AIO_USERNAME, AIO_KEY, AIO_FEED_IDs, callBackFunc_Message)
client.setup()
client.connect_and_loop()

import json

def read_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_data_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
while True:
    id = uuid.uuid4()
    print(id)
    pass