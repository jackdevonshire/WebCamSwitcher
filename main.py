import cv2
import pyvirtualcam as pyvirtualcam
from gaze_tracking import GazeTracking

global CurrentlyScanning
global CurrentlyLive

gaze = GazeTracking()

#########################################
CurrentlyScanning = "left"
CurrentlyLive = "center"

webcams = {
    "left": cv2.VideoCapture(0),
    "center": cv2.VideoCapture(1)
}

# The percentage of measurements within 0 to tick_range that need detect face looking at it, required to switch cameras
accuracy = 0.8
tick_range = 20
#########################################
measurements = [False] * tick_range

# Initialising Webcam Selection
scanning_webcam = webcams[CurrentlyScanning]
live_webcam = webcams[CurrentlyLive]

# Starting virtual camera
width = int(live_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(live_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
with pyvirtualcam.Camera(width=width, height=height, fps=60) as virtual_cam:
    while True:
        # Webcam selection
        scanning_webcam = webcams[CurrentlyScanning]
        live_webcam = webcams[CurrentlyLive]

        # Get frames from the live and scanning webcam
        _, scanning_frame = scanning_webcam.read()
        _, live_frame = live_webcam.read()

        # Detect gaze using GazeTracking module
        gaze.refresh(scanning_frame)


        if gaze.is_center():
            # If the average of the last positive detection measurements (looking at scanning camera) meets the
            # accuracy threshold
            average_positive_detections = sum(measurements) / tick_range

            if average_positive_detections >= accuracy:
                # Reset looking at camera count
                looking_at_camera_count = 0

                # Switch scanning and live cameras based on which camera has detected gaze looking at it
                if CurrentlyScanning == "center":
                    CurrentlyScanning = "left"
                    CurrentlyLive = "center"
                elif CurrentlyScanning == "left":
                    CurrentlyScanning = "center"
                    CurrentlyLive = "left"

            measurements.append(True)
        else:
            measurements.append(False)

        # Only want the last x measurements (between 0 and tick_range)
        if len(measurements) > tick_range:
            measurements.pop(0)

        # Pipe frames through to virtual camera
        virtual_frame = cv2.resize(live_frame, (width, height))
        virtual_frame = cv2.cvtColor(virtual_frame, cv2.COLOR_RGB2BGR)  # Convert if needed
        virtual_cam.send(virtual_frame)

        if cv2.waitKey(1) == 27:
            break
