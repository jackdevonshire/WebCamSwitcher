config = {
    # General Setup
    "webcam_ids": [0, 1],  # The device id's of all webcams the system can access
    "measurement_range": 30,  # Amount of measurements used to determine which camera to select
    "cooldown_seconds": 1,  # After switching camera, block switching cameras for x seconds
    "centre_webcam": 1, # The script tries to account for the centre webcam having the best view of you most of the time

    # Virtual Camera Output
    "virtual_cam_width": 1080,
    "virtual_cam_height": 1080,
    "virtual_cam_fps": 60,

    "debug": True
}