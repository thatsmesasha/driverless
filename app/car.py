import sys
from threading import Timer
import time
import json
import os

class Car:
    config = {}

    speed = None
    steering = None
    duration = None

    timer_to_stop = None

    last_direction = None

    def __init__(self):
        self.initialize()

    def initialize(self):
        if Car.speed is None or Car.steering is None:
            try:
                from gpiozero import Servo
                from aiy.pins import PIN_A
                from aiy.pins import PIN_B
                Car.speed = Servo(PIN_B)
                Car.steering = Servo(PIN_A)
                Car.connected = True
            except:
                self.log('ERROR', 'Driving is not supported')
                Car.connected = False
        if len(Car.config.keys()) == 0:
            Car.load_config()

        return Car.connected

    @staticmethod
    def log(level, message):
        now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
        print('{} - - [{}] {}'.format(level, now, message))

    @classmethod
    def load_config(cls):
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
            cls.config = json.load(f)

    def get_config(self):
        return Car.config

    @classmethod
    def _drive(cls, direction, canceling_last=False):
        if canceling_last:
            cls.timer_to_stop = None

        cls.log('INFO', 'Driving in direction "{}"'.format(direction))
        cls.speed.value = cls.config[direction]['speed']
        if direction != 'stop':
            cls.steering.value = cls.config[direction]['steering']

    def drive(self, direction):
        if not self.initialize():
            return None

        if direction not in Car.config.keys():
            raise Exception('Direction "{}" not in {}'.format(direction, Car.config.keys()))

        # overwrite last direction
        if Car.timer_to_stop:
            Car.timer_to_stop.cancel()
            Car.timer_to_stop = None

        Car._drive(direction)

        # to go back the car first needs to stop
        if direction == 'back' and Car.last_direction != 'back':
            Timer(0.05, lambda: Car._drive('stop')).start()
            Timer(0.15, lambda: Car._drive(direction)).start()

        Car.last_direction = direction

        # stop after duration of driving
        if direction != 'stop':
            Car.timer_to_stop = Timer(Car.config[direction]['duration'],
                lambda: Car._drive('stop', canceling_last=True))
            Car.timer_to_stop.start()

            return Car.config[direction]['duration']

        return None
