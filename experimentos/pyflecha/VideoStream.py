from webcamvideostream import WebcamVideoStream

class VideoStream:
    def __inti__(self, src=0, usePiCamera=False, resolution=(320,240),
                 framerate=32):
        if usePiCamera:
            from pivideostream import PiVideoStream
            self.stream = PiVideoStream(resolution=resolution,
                                        framerate=framerate)
        else:
            self.stream = WebcamVideoStream(src=src)

    def start(self):
        return self.stream.start()

    def update(self):
        self.stream.update()

    def read(self):
        self.stream.read()

    def stop(self):
        self.stream.stop()
