from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from .car import Car
from .main import main as main_blueprint
from .control import control as control_blueprint

def create_app():
    app = Flask(__name__)

    app.secret_key = "super secret key"

    bootstrap = Bootstrap(app)

    app.register_blueprint(control_blueprint, url_prefix='/control')
    app.register_blueprint(main_blueprint)

    print(' * INFO Initializing the car, this may take several seconds...')
    Car()
    if Car.connected:
        print(' * INFO Initialized the car successfully')
    else:
        print(' * INFO Driving is not connected')

    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=4242)
