import cv2
import pyvirtualcam

from Camera import Camera

### Config ###

webcamIds = [0, 1] # Device ids of all webcams
measurement_range = 15 # Amount of measurements to base camera switching decisions off of

virtual_cam_width = 640
virtual_cam_height = 480
virtual_cam_fps = 60

### Main Program ###

# First initialise all webcams
webcams = []
for webcamId in webcamIds:
    camera = Camera("", webcamId, measurement_range)
    webcams.append(camera)

# Now load virtual webcam and initialise main program loop
with pyvirtualcam.Camera(width=virtual_cam_width, height=virtual_cam_height, fps=virtual_cam_fps) as virtual_cam:
    while True:
        best_detections = 0
        best_frame = None

        # Select the best frame based on the webcam with the most positive detections for given measurement range
        for webcam in webcams:
            current_frame = webcam.get_frame()
            current_detections = webcam.get_positive_detections()

            if current_detections > best_detections:
                best_detections = current_detections
                best_frame = current_frame

        # Format best frame for virtual camera
        virtual_frame = best_frame
        virtual_frame = cv2.cvtColor(virtual_frame, cv2.COLOR_RGB2BGR)  # Convert frame colour for virtual webcam
        virtual_frame = cv2.resize(virtual_frame, (virtual_cam_width, virtual_cam_height))

        # Sent frame to virtual camera
        virtual_cam.send(best_frame)