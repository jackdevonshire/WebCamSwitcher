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

sensitivity = 10 # Higher = More Precise, Slower Switching. Vice versa.
#########################################

# Initialising Webcam Selection
scanning_webcam = webcams[CurrentlyScanning]
live_webcam = webcams[CurrentlyLive]

# Starting virtual camera
width = int(live_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(live_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
with pyvirtualcam.Camera(width=width, height=height, fps=60) as virtual_cam:
    looking_at_camera_count = 0
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
            looking_at_camera_count += 1

            # If continuously looked at scanning camera for x period of time,
            # switch that to be the live camera
            if looking_at_camera_count > sensitivity:
                # Reset looking at camera count
                looking_at_camera_count = 0

                print("Detected looking at current camera")

                # Switch scanning and live cameras based on which camera has detected gaze looking at it
                if CurrentlyScanning == "center":
                    CurrentlyScanning = "left"
                    CurrentlyLive = "center"
                elif CurrentlyScanning == "left":
                    CurrentlyScanning = "center"
                    CurrentlyLive = "left"

        else:
            looking_center_count = 0

        # Pipe frames through to virtual camera
        virtual_frame = cv2.resize(live_frame, (width, height))
        virtual_frame = cv2.cvtColor(virtual_frame, cv2.COLOR_RGB2BGR)  # Convert if needed
        virtual_cam.send(virtual_frame)

        if cv2.waitKey(1) == 27:
            break
