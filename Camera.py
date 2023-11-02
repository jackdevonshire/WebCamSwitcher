import cv2
from gaze_tracking import GazeTracking


class Camera:
    def __init__(self, label, device_id, measurement_range):
        self.label = label
        self.webcam_instance = cv2.VideoCapture(device_id)
        self.gaze = GazeTracking()

        self.measurement_range = measurement_range
        self.measurements = [False]*measurement_range

    def get_frame(self):
        _, frame = self.webcam_instance.read() # Get frame from camera
        self.gaze.refresh(frame) # Scan for gaze detection data
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # Convert frame colour for virtual webcam

        current_measurement = self.gaze.is_center() # Detect whether user is looking at this camera

        # Adjust current list of measurements to get average measurements
        self.measurements.append(current_measurement)
        if len(self.measurements) > self.measurement_range:
            self.measurements.pop(0)

        return frame

    def get_average_measurements(self):
        return self.measurements / self.measurement_range


