from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from .car import Car
from .camera import Camera
from .model import Model
from .main import main as main_blueprint
from .control import control as control_blueprint
import time

def log(level, message):
    now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
    print('{} - - [{}] {}'.format(level, now, message))

def init_car():
    log('INFO', 'Initializing the car, this may take several seconds...')
    Car()
    if Car.connected:
        log('INFO', 'Initialized the car successfully')
    else:
        log('INFO', 'Driving is not connected')

def init_camera():
    log('INFO', 'Initializing the camera, this may take several seconds...')
    Camera()
    if Camera.connected:
        log('INFO', 'Initialized the camera successfully')
    else:
        log('INFO', 'Camera is not connected')

def init_self_driving():
    log('INFO', 'Initializing the model, this may take several seconds...')
    Model()
    if Model.good:
        log('INFO', 'Initialized self-driving successfully')
    else:
        log('INFO', 'Self-driving is not available')

def create_app():
    app = Flask(__name__)

    app.secret_key = "super secret key"

    bootstrap = Bootstrap(app)

    app.register_blueprint(control_blueprint, url_prefix='/control')
    app.register_blueprint(main_blueprint)

    init_car()
    init_camera()
    init_self_driving()

    return app

if __name__ == '__main__':
    create_app().run(debug=False, host='0.0.0.0', port=4242)
