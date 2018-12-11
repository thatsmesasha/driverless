from PIL import Image
import time
from io import BytesIO
import sys, os, io
from threading import Thread
from .car import Car

# filename of the model that is placed in /opt/aiy/models
MODEL_NAME = 'car.binaryproto'

labels = ['forward', 'left', 'right']

class Model:
    model = None
    car = None
    inference_engine = None
    model_name = None
    on = False

    good = False

    name = 'mobilenet_160'
    input_shape = (1, 160, 160, 3)
    input_normalizer = (128.0, 128.0)

    thread = None

    def __init__(self):
        self.initialize()

    def initialize(self):
        if Model.car is None:
            car = Car()
            if Car.connected:
                Model.car = car
                self.log('INFO', 'Car for self-driving is connected')
            else:
                self.log('ERROR', 'Car is not connected for self-driving')
                return False

        if Model.model is None:
            try:
                from aiy.vision import inference
                from aiy.vision.models import utils

                Model.model = inference.ModelDescriptor(
                    name='mobilenet_160',
                    input_shape=(1, 160, 160, 3),
                    input_normalizer=(128.0, 128.0),
                    compute_graph=utils.load_compute_graph(MODEL_NAME))
                self.log('INFO', 'Self-driving model is loaded')
            except Exception as e:
                self.log('ERROR', 'Self-driving model cannot be loaded: {}'.format(str(e)))
                return False

        if Model.inference_engine is None:
            try:
                from aiy.vision import inference
                Model.inference_engine = inference.InferenceEngine()
                try:
                    Model.inference_engine.unload_model('mobilenet_160')
                except:
                    pass
                Model.model_name = Model.inference_engine.load_model(Model.model)
                Model.good = True
                self.log('INFO', 'Image inference has started')
            except Exception as e:
                self.log('ERROR', 'Image inference cannot be started: {}'.format(str(e)))
                return False

        return True

    def start(self):
        if Model.thread:
            return True

        if not self.initialize():
            return False

        Model.on = True
        Model.thread = Thread(target=self._thread)
        Model.thread.start()

    def end(self):
        Model.on = False
        Model.thread = None

    @classmethod
    def process(cls, result):
        """Processes inference result and returns labels sorted by confidence."""
        assert len(result.tensors) == 1
        tensor = result.tensors['final_result']
        probs, shape = tensor.data, tensor.shape
        try:
            assert shape.depth == len(labels)
        except:
            print(shape.depth)
        assert shape.depth == len(labels)
        #0.1 is a threshold, if the score is less then that confidence level is to low
        pairs = [pair for pair in enumerate(probs) if pair[1] > 0.1]
        pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
        return labels[pairs[0][0]], pairs[0][1]


    @classmethod
    def _thread(cls):
        try:
            cls.log('INFO', 'Start self-driving')
            try:
                cls.inference_engine.start_camera_inference(cls.model_name)
            except StartCameraInference:
                pass
            while cls.on:
                result = cls.inference_engine.camera_inference()
                direction, probability = cls.process(result)
                cls.log('INFO', 'Predicted direction {} with probability {:.3f}%'.format(direction, probability * 100))
                cls.car.drive(direction)
            cls.inference_engine.stop_camera_inference()
        except Exception as e:
            cls.log('EXCEPTION', e)
            try:
                cls.inference_engine.stop_camera_inference()
            except:
                pass
        cls.log('INFO', 'Stopped self-driving')


    @staticmethod
    def log(level, message):
        now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
        print('{} - - [{}] {}'.format(level, now, message))
