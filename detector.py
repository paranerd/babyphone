import time
import numpy as np
import cv2
import threading
from collections import deque

from logger import Logger
from supplier import Supplier

class Detector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = Logger("Detector")
        self.name = self.__class__.__name__

        self.supplier = Supplier()
        self.supplier.start()
        self.current_frame = None
        self.fps = self.supplier.get_fps()

        # Notification
        self.notified_at = 0
        self.seconds_between_notifications = 5

        self.OBSERVER_LENGTH = 5 # Time in seconds to be observed for motion
        self.threshold = 0.4

    def __del__(self):
        print("Destroying all windows")
        # Stop supplier
        if self.supplier:
            self.supplier.set_stop()

    def run(self):
        """
        Main worker
        """
        observer = deque(maxlen=self.fps * self.OBSERVER_LENGTH)
        previous_frame = None

        while True:
            self.current_frame = self.supplier.get_frame()

            if self.current_frame is None:
                continue

            # Gray frame
            frame_gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)

            # Blur frame
            frame_blur = cv2.GaussianBlur(frame_gray, (21, 21), 0)

            # If there's no previous frame, use the current one
            if previous_frame is None:
                previous_frame = frame_blur
                continue

            # Delta frame
            delta_frame = cv2.absdiff(previous_frame, frame_blur)

            # Threshold frame
            threshold_frame = cv2.threshold(delta_frame, 15, 255, cv2.THRESH_BINARY)[1]

            # Dilate the thresholded image to fill in holes
            kernel = np.ones((5, 5), np.uint8)
            dilated_frame = cv2.dilate(threshold_frame, kernel, iterations=4)

            # Find difference in percent
            res = dilated_frame.astype(np.uint8)
            movement = (np.count_nonzero(res) * 100) / res.size

            # Add movement percentage to observer
            observer.append(movement)

            if self.notified_at < time.time() - self.seconds_between_notifications and sum([x > self.threshold for x in observer]) > 0:
                self.notify()
                self.logger.info("Motion detected!")

            # Set blurred frame as new previous frame
            previous_frame = frame_blur

            # Exit on 'q'
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                self.supplier.set_stop()
                print("Exiting...")
                break

    def notify(self):
        self.notified_at = time.time()
        self.logger.info("Notifying...")

if __name__ == "__main__":
    d = Detector()
    d.start()