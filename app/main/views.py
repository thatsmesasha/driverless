from flask import render_template, Response, send_from_directory
from . import main

@main.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@main.route('/about', methods=['GET'])
def about():
    return render_template('/about.html')

@main.route('/settings', methods=['GET'])
def settings():
    return render_template('/settings.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    try:
        from ..camera import Camera
        return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        print('Camera not supported')
        return send_from_directory('static', filename='img/video_feed_sample.jpg')
