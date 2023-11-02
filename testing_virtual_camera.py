import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()

global CurrentlyScanning
CurrentlyScanning = "center"

webcams = {
    "left": cv2.VideoCapture(0),
    "center": cv2.VideoCapture(1)
}

# The higher this is, the more precise gaze detection will be, but it will be slower to switch cameras
sensitivity = 20

looking_at_camera_count = 0
while True:
    webcam = webcams[CurrentlyScanning]
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()
    text = ""

    if gaze.is_center():
        looking_at_camera_count += 1

        if looking_at_camera_count > sensitivity:
            # Reset looking at camera count
            looking_at_camera_count = 0

            print("Detected looking at current camera")

            # Switch the webcam we are scanning
            if CurrentlyScanning == "center":
                CurrentlyScanning = "left"
            else:
                CurrentlyScanning = "center"

            # Switch the OBS scene
            #
            #
            #
    else:
        looking_center_count = 0

    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)

    if cv2.waitKey(1) == 27:
        break
