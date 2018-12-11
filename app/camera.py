import time
import io
from threading import Timer, Thread
import os
from PIL import Image
from pathlib import Path
import time

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    resolution = (160, 160)

    label = None
    last_label = None
    folder = None
    remove_label_timer = None

    frames = []

    def __init__(self):
        self.initialize()

    def initialize(self):
        if Camera.thread is None:
            # check if can connect to the camera
            try:
                import picamera
                with picamera.PiCamera() as camera:
                    pass
            except:
                Camera.connected = False
                return False

            # start background frame thread
            Camera.thread = Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
        Camera.connected = True
        return True

    def get_frame(self):
        self.initialize()
        return self.frame

    @staticmethod
    def log(level, message):
        now = time.strftime('%d/%b/%y %H:%M:%S.{}'.format(str(time.time() % 1)[2:5]))
        print('{} - - [{}] {}'.format(level, now, message))

    @classmethod
    def _thread(cls):
        try:
            import picamera
            with picamera.PiCamera() as camera:
                # camera setup
                camera.resolution = cls.resolution

                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg',
                                                     use_video_port=True):
                    # store frame
                    stream.seek(0)
                    cls.frame = stream.read()



                    # store only during driving
                    if cls.label:
                        cls.frames.append((time.time(), cls.frame))

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()
        except Exception as e:
            cls.log('EXCEPTION', e)
            return

    @staticmethod
    def save(timestamp, frame, label, foldername):
        # save to root
        directory = os.path.join(str(Path(os.path.dirname(__file__)).parent), 'data', foldername, label)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, str(int(timestamp * 1000)) + '.jpeg')
        Image.open(io.BytesIO(frame)).save(filename)

    @staticmethod
    def save_several(frames, label, foldername):
        for timestamp, frame in frames:
            Camera.save(timestamp, frame, label, foldername)


    def add_label(self, new_label, new_duration, folder=None):
        if not self.initialize():
            return

        if Camera.remove_label_timer:
            Camera.remove_label_timer.cancel()

        Camera.label = new_label
        Camera.folder = folder

        Camera.remove_label_timer = Timer(new_duration, Camera.remove_label)
        Camera.remove_label_timer.start()

        if Camera.last_label == new_label and folder:
            self.log('INFO', 'Last label was the same, saving {} pictures in between...'.format(len(Camera.frames)))
            Thread(target=lambda: self.save_several(Camera.frames, new_label, folder)).start()
        elif folder:
            # switched direction on the car, so save images in between to "unlabeled" category
            Thread(target=lambda: self.save_several(Camera.frames, 'unlabeled', folder)).start()


        Camera.last_label = new_label

        # save first picture when driving started
        if folder:
            Thread(target=lambda: Camera.save(time.time(), Camera.frame, new_label, Camera.folder)).start()
        Camera.frames = []

    @classmethod
    def remove_label(cls):
        cls.label = None
        cls.folder = None
        cls.remove_label_timer = None
