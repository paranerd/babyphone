import threading
import cv2

class Supplier(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.name = self.__class__.__name__

        self.current_frame = None

        # Time in seconds to be observed for motion
        self.OBSERVER_LENGTH = 5

        # Set RTSP stream as source
        self.username = "admin"
        self.password = ""
        self.ip = ""
        self.port = 554
        self.source = cv2.VideoCapture("rtsp://{}:{}@{}:{}//h264Preview_01_main".format(self.username, self.password, self.ip, self.port))

        # Set FPS (default: 36)
        self.fps = self.determine_fps(self.source)

        self.do_stop = False

        self.height, self.width = self.get_dimensions()

    def __del__(self):
        # Release camera
        self.source.release()

        # Close all windows
        cv2.destroyAllWindows()

    def determine_fps(self, source):
            """
            Determine frames per second of the video source

            @param video source
            @return int
            """
            Util.log(self.name, "Determining FPS...")

            # How many frames to capture
            num_frames = 120

            # Start time
            start = time.time()

            # Grab a few frames
            for i in range(0, num_frames):
                ret, frame = source.read()

            # End time
            end = time.time()

            # Calculate frames per second
            fps = int(math.floor(num_frames / (end - start)))
            Util.log(self.name, "Setting FPS to " + str(fps))

            return fps

    def get_fps(self):
        """
        Returns source FPS

        @return int
        """
        return self.fps

    def get_frame(self):
        """
        Return the current frame

        @return bytes
        """
        #return self.frame_to_jpg(self.current_frame) if self.current_frame is not None else None
        return self.current_frame if self.current_frame is not None else None

    def frame_to_jpg(self, frame):
        """
        Convert video frame to jpg

        @param array frame
        @return bytes
        """
        ret, jpeg = cv2.imencode('.jpg', self.current_frame)
        return jpeg.tobytes()

    def get_dimensions(self):
        """
        Determine height and width of the video source

        @return tuple(int, int)
        """
        frame = cv2.cvtColor(self.source.read()[1],cv2.COLOR_RGB2GRAY)
        return frame.shape[0: 2]

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def set_stop(self):
        self.do_stop = True

    def run(self):
        """
        Main worker
        """
        previous_frame = None

        while True:
            # Grab a frame
            (grabbed, self.current_frame) = self.source.read()

            # End of feed
            if not grabbed:
                break

            if self.do_stop:
                print("Supplier stopping (breaking)...")
                break

if __name__ == "__main__":
    s = Supplier()
    s.start()
