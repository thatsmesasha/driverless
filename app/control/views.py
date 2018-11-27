from flask import render_template, request, json, Response, send_from_directory
from . import control
import time
import json
import os
from pathlib import Path
from ..car import Car
from ..camera import Camera

@control.route('/drive', methods=['POST'])
def drive():
    direction = request.json.get('direction')
    print('Debug received request to drive in the direction "{}"'.format(direction))
    car = Car()
    if not Car.connected:
        return json.dumps({ 'error': 'Driving is not connected' })

    camera = Camera()

    end_driving = car.drive(direction)
    if Camera.connected and direction != 'stop':
        camera.new_end_recording = end_driving
        camera.new_label = direction

    return json.dumps(True)

@control.route('/update-settings', methods=['POST'])
def update_settings():
    print(request.form)

    config = {
        'forward': {
            'speed': float(request.form['speed-forward']),
            'steering': float(request.form['steering-forward']),
            'duration': float(request.form['duration-forward']),
        },
        'left': {
            'speed': float(request.form['speed-left']),
            'steering': float(request.form['steering-left']),
            'duration': float(request.form['duration-left']),
        },
        'right': {
            'speed': float(request.form['speed-right']),
            'steering': float(request.form['steering-right']),
            'duration': float(request.form['duration-right']),
        },
        'back': {
            'speed': float(request.form['speed-back']),
            'steering': float(request.form['steering-back']),
            'duration': float(request.form['duration-back']),
        },
        'stop': {
            'speed': 0,
            'steering': 0,
            'duration': 0,
        },
    }
    with open(os.path.join(str(Path(os.path.dirname(__file__)).parent), 'config.json'), 'w') as f:
        json.dump(config, f)
    now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
    print('INFO - - [{}] {}'.format(now, 'Updated car settings'))

    Car.load_config()

    return json.dumps(True)
