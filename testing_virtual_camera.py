import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()

global CurrentlyScanning
global CurrentlyLive
CurrentlyScanning = "left"
CurrentlyLive = "center"

webcams = {
    "left": cv2.VideoCapture(0),
    "center": cv2.VideoCapture(1)
}

# The higher this is, the more precise gaze detection will be, but it will be slower to switch cameras
sensitivity = 20

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

    # Pipe live camera frames
    cv2.putText(live_frame, "", (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", live_frame)

    if cv2.waitKey(1) == 27:
        break
