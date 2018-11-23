from gpiozero import Servo
from aiy.pins import PIN_A
from aiy.pins import PIN_B
import sys
from threading import Timer
import time

class Car:
    speed_of = { 'forward': 0.2, 'right': 0.2, 'left': 0.2, 'back': -0.3, 'stop': 0 }
    steering_of = { 'forward': 0, 'right': -1, 'left': 1, 'back': 0, 'stop': 0 }
    duration_of = { 'forward': 0.5, 'right': 0.5, 'left': 0.5, 'back': 0.5 }
    directions = speed_of.keys()

    speed = None
    steering = None
    duration = None

    timer_to_stop = None

    last_direction = None

    def initialize(self):
        if Car.speed is None:
            Car.speed = Servo(PIN_B)
        if Car.steering is None:
            Car.steering = Servo(PIN_A)

    @classmethod
    def _drive(cls, direction, canceling_last=False):
        if canceling_last:
            print('Debug last direction has ended')
            cls.timer_to_stop = None

        print('Debug driving in direction "{}"'.format(direction))
        cls.speed.value = cls.speed_of[direction]
        cls.steering.value = cls.steering_of[direction]

    def drive(self, direction):
        self.initialize()
        if direction not in Car.directions:
            raise Exception('Direction "{}" not in {}'.format(direction, Car.directions))

        Car._drive(direction)

        # to go back the car first needs to stop
        if direction == 'back' and Car.last_direction not in ['back', 'stop']:
            Timer(0.05, lambda: Car._drive('stop')).start()
            Timer(0.10, lambda: Car._drive(direction)).start()

        # overwrite last direction
        if Car.timer_to_stop:
            Car.timer_to_stop.cancel()
            Car.timer_to_stop = None
            print('Debug canceled last timer to stop')

        # stop after duration of driving
        if direction != 'stop':
            Car.timer_to_stop = Timer(Car.duration_of[direction],
                lambda: Car._drive('stop', canceling_last=True))
            Car.timer_to_stop.start()

            print('Debug created new timer to stop in {}s'.format(Car.duration_of[direction]))
            return time.time() + Car.duration_of[direction]

        Car.last_direction = direction

        return None
