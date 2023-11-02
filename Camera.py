import cv2
from gaze_tracking import GazeTracking


class Camera:
    def __init__(self, label, device_id, measurement_range):
        self.label = label
        self.webcam_instance = cv2.VideoCapture(device_id)
        self.gaze = GazeTracking()

        self.measurement_range = measurement_range
        self.measurements = [False]*measurement_range

        # Startup to ensure camera has a frame available
        self.l__ast_frame = None
        self.update_model()

    def get_last_frame(self):
        return self.last_frame

    def update_model(self):
        _, frame = self.webcam_instance.read() # Get frame from camera
        self.gaze.refresh(frame) # Scan for gaze detection data

        current_measurement = bool(self.gaze.is_center()) # Detect whether user is looking at this camera

        # Adjust current list of measurements to get average measurements
        self.measurements.append(current_measurement)
        if len(self.measurements) > self.measurement_range:
            self.measurements.pop(0)

        self.last_frame = frame

        return sum(self.measurements)


