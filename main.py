import threading
import time
import cv2
import pyvirtualcam

from Camera import Camera
from config import config

global can_switch_cameras
can_switch_cameras = True


# This function allows for a cooldown timer between switching cameras
def cooldown_timer():
    global can_switch_cameras

    can_switch_cameras = False
    time.sleep(config["cooldown_seconds"])
    can_switch_cameras = True


def initialise_webcams():
    webcams = []
    for webcamId in config["webcam_ids"]:
        camera = Camera("", webcamId, config["measurement_range"])
        webcams.append(camera)

    return webcams


def update_virtual_camera(virtual_cam, best_frame):
    # Format best frame for virtual camera
    virtual_frame = best_frame
    virtual_frame = cv2.resize(virtual_frame, (config["virtual_cam_width"], config["virtual_cam_height"]))
    virtual_frame = cv2.cvtColor(virtual_frame, cv2.COLOR_RGB2BGR)  # Convert frame colour for virtual webcam

    # Send frame to virtual camera
    virtual_cam.send(virtual_frame)


def main():
    # Initialise all webcams
    webcams = initialise_webcams()

    current_best_webcam = webcams[0]

    # Now load virtual webcam and initialise main program loop
    with pyvirtualcam.Camera(width=config["virtual_cam_width"], height=config["virtual_cam_height"],
                             fps=config["virtual_cam_fps"]) as virtual_cam:
        while True:
            # This is the furthest a user can be looking from a camera, as the range is 0 to 1, with 0.5 being centre
            best_detections = 0.5*config["measurement_range"]
            start_cooldown = False

            if can_switch_cameras:
                # Select the best frame based on the webcam with the most positive detections for given measurement range
                for webcam in webcams:
                    current_detections = webcam.update_model()

                    if current_detections < best_detections:
                        # If we're going to switch webcams, start a cooldown timer before switching again
                        if current_best_webcam != webcam:
                            start_cooldown = True

                        best_detections = current_detections
                        current_best_webcam = webcam
            else:
                current_best_webcam.update_model()

            best_frame = current_best_webcam.get_last_frame()
            update_virtual_camera(virtual_cam, best_frame)

            if start_cooldown:
                threading.Thread(target=cooldown_timer).start()


if __name__ == "__main__":
    main()
