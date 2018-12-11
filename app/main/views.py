from flask import render_template, Response, send_from_directory
from . import main
import time
from ..car import Car
from ..camera import Camera

@main.route('/', methods=['GET'])
def index():
    config = Car().get_config()
    car_connected = Car.connected

    now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
    print('INFO - - [{}] Car {} connected'.format(now, 'is' if car_connected else 'is not'))

    Camera()
    camera_connected = Camera.connected

    now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
    print('INFO - - [{}] Camera {} connected'.format(now, 'is' if camera_connected else 'is not'))

    return render_template('/index.html', car_connected=car_connected, camera_connected=camera_connected, config=config)

@main.route('/about', methods=['GET'])
def about():
    return render_template('/about.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    camera = Camera()
    if Camera.connected:
        return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

    now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
    return send_from_directory('static', filename='img/video_feed_sample.jpg')
