import cv2
from gaze_tracking import GazeTracking
from config import config

debug = False

class Camera:
    def __init__(self, label, device_id, measurement_range):
        self.label = label
        self.device_id = device_id
        self.webcam_instance = cv2.VideoCapture(device_id)
        self.gaze = GazeTracking()

        self.measurement_range = measurement_range
        self.measurements = [0.5]*measurement_range

        self.centre_webcam = config["centre_webcam"] == device_id

        # Startup to ensure camera has a frame available
        self.last_frame = None
        self.update_model()

    def get_last_frame(self):
        if config["debug"]:
            return self.gaze.annotated_frame()

        return self.last_frame

    def update_model(self):
        _, frame = self.webcam_instance.read() # Get frame from camera
        try:
            self.gaze.refresh(frame) # Scan for gaze detection data
            # Detect where user is looking. 0 = Right, 0.5 = Camera, 1 = Left
            horizontal_ratio = self.gaze.horizontal_ratio()
            amount_off_centre = abs(0.5 - horizontal_ratio)

        except:
            amount_off_centre = 1

        if self.centre_webcam:
            amount_off_centre += 0.1

        # Adjust current list of measurements to get average measurements
        self.measurements.append(amount_off_centre)

        if len(self.measurements) > self.measurement_range:
            self.measurements.pop(0)

        self.last_frame = frame

        return sum(self.measurements)


