import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()

global CurrentlyScanning
CurrentlyScanning = "center"

webcam_ids = {
    "left": 0,
    "center": 1
}

looking_at_camera_count = 0
webcam = cv2.VideoCapture(webcam_ids[CurrentlyScanning])
while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()
    text = ""

    if gaze.is_center():
        looking_at_camera_count += 1

        if looking_at_camera_count > 20:
            # Reset looking at camera count
            looking_at_camera_count = 0

            print("Detected looking at current camera")
            # Release the current webcam being scanned
            webcam.release()

            # Switch the webcam we are scanning
            if CurrentlyScanning == "center":
                webcam = cv2.VideoCapture(webcam_ids["left"])
                CurrentlyScanning = "left"
            else:
                webcam = cv2.VideoCapture(webcam_ids["center"])
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
