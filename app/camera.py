import time
import io
import threading
import os
from PIL import Image

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    resolution = (160, 160)

    label = None
    new_label = None

    end_recording = None
    new_end_recording = None

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
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
        Camera.connected = True
        return True

    def get_frame(self):
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
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

                # if driving has ended
                if cls.label and cls.end_recording < time.time():
                    cls.label = None
                    cls.end_recording = None
                    cls.recording = False

                # if new driving
                if cls.new_label:
                    cls.end_recording = cls.new_end_recording
                    cls.new_end_recording = None

                    # if last label was the same, save all pictures in between
                    if cls.label == cls.new_label and cls.folder:
                        for timestamp, frame in cls.frames:
                            cls.save(timestamp, frame, cls.label, cls.folder)

                    # save first picture when driving started
                    if cls.folder:
                        cls.save(time.time(), cls.frame, cls.new_label, cls.folder)
                    cls.frames = []

                    cls.label = cls.new_label
                    cls.new_label = None


                # capture only during driving
                if cls.label:
                    cls.frames.append((time.time(), cls.frame))

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    @classmethod
    def thread_stop(cls):
        cls.thread = None

    @classmethod
    def save(cls, timestamp, frame, label, foldername):
        directory = os.path.join(os.getcwd(), foldername, label)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, str(int(timestamp * 1000)) + '.jpeg')
        Image.open(frame).save(filename)
