from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)

    app.secret_key = "super secret key"

    bootstrap = Bootstrap(app)

    from .main import main as main_blueprint
    from .control import control as control_blueprint
    app.register_blueprint(control_blueprint, url_prefix='/control')
    app.register_blueprint(main_blueprint)

    try:
        print('Debug initializing the car, this may take several seconds...')
        from .car import Car
        Car().initialize()
        print('Debug initialized the car successfully')
    except Exception as e:
        print('Error initializing the car: {}'.format(e))

    return app
