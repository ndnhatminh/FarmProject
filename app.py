from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import numpy as np
import time
from dotenv import dotenv_values
from adafruit_mqtt import Adafruit_MQTT
import json

def rain_prediction(temp, humidi):
    theta = np.load('model_params.npy')

    new_data = np.array([[temp, humidi, 1]])

    # Dự đoán lượng mưa cho dữ liệu mới
    prediction = new_data.dot(theta)

    pre = prediction[0][0]
    return 0 if pre < 0 else pre

print("rain prediction", rain_prediction(25,0.7))


def read_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_data_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def delete_data_to_json(file_path, id):
    print("id:", id)
    data = read_data_from_json(file_path)
    print("data:", type(data['schedule']))
    for item in data['schedule']:
        if item[0] == int(id):
            schedule = {
                "code": "delete",
                "id": int(id),
                "mixer1": item[2],
                "mixer2": item[3],
                "mixer3": item[4],
                "cycle": item[5],
                "area": item[6],
                "start time": item[7]
            }
            response_data_string = json.dumps(schedule)

            client.publish('schedule', response_data_string)
            data['schedule'].remove(item)
    print('deleted', data['schedule'])
    write_data_to_json(data, file_path)

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

# # MAIN PROGRAM
# # Create an instance of Adafruit_MQTT class
client = Adafruit_MQTT(AIO_USERNAME, AIO_KEY, AIO_FEED_IDs, callBackFunc_Message)
client.setup()
client.connect_and_loop()

app = Flask(__name__)

def save_scheduler():
    # Add logic to start fertilizer process
    pass

@app.route('/')
def index():
    data = read_data_from_json('data.json')
    temp = data['temp']
    humi = data['humi']

    print("temp in api:", temp)

    data = read_data_from_json('data.json')
    schedule = data['schedule']

    rain = rain_prediction(temp, humi)
    return render_template('index.html', temp=temp, humi=humi, schedule=schedule, rain=rain)

@app.route('/delete', methods=['POST'])
def delete_schedule():
    data = request.json
    schedule_id = data.get('id')
    delete_data_to_json('data.json', schedule_id)
    print(schedule_id)
    # return jsonify({'message': 'Schedule deleted successfully'})
    return redirect(url_for('index'))

@app.route('/scheduler', methods=['POST'])
def scheduler():
    schedule_name = request.form['scheduleName']
    flow_1 = request.form['flow1']
    flow_2 = request.form['flow2']
    flow_3 = request.form['flow3']
    cycle = request.form['cycle']
    # water_amount = request.form['waterAmount']
    watering_area = request.form['wateringArea']
    start_time = request.form['startTime']
    id = int(time.time()*1000)

    response_data = {
        "code": "create",
        "id": id,
        "mixer1": flow_1,
        "mixer2": flow_2,
        "mixer3": flow_3,
        "cycle": cycle,
        "area": watering_area,
        "start time": start_time
    }

    schedule = [id, schedule_name, flow_1, flow_2, flow_3, cycle, watering_area, start_time]
    response_data_string = json.dumps(response_data)

    client.publish('schedule', response_data_string)

    data = read_data_from_json('data.json')
    data['schedule'].append(schedule)
    write_data_to_json(data, 'data.json')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)