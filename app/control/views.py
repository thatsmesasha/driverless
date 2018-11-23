from flask import render_template, request, json, Response, send_from_directory
from . import control

@control.route('/drive', methods=['POST'])
def drive():
    direction = request.json.get('direction')
    print('Debug received request to drive in the direction "{}"'.format(direction))
    try:
        from ..car import Car
        car = Car()
    except Exception as e:
        detailed_error = 'Error during initialization of car object: {}'.format(e)
        print(detailed_error)
        error = 'Cannot connect to the car'
        return json.dumps({ 'error': error, 'detailed_error': detailed_error })

    try:
        from ..camera import Camera
        camera = Camera()
    except Exception as e:
        detailed_error = 'Error during initialization of camera object: {}'.format(e)
        print(detailed_error)
        camera = None

    try:
        end_driving = car.drive(direction)
        if camera and direction != 'stop':
            camera.new_end_recording = end_driving
            camera.new_label = direction
    except Exception as e:
        detailed_error = 'Error during driving: {}'.format(e)
        print(detailed_error)
        error = 'Unexpected error occured, please refresh the page'
        return json.dumps({ 'error': error, 'detailed_error': detailed_error })

    return json.dumps(True)
