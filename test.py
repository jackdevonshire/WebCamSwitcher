import pyvirtualcam

### Config ###

webcamIds = [0, 1] # Device ids of all webcams
measurement_range = 15 # Amount of measurements to base camera switching decisions off of

virtual_cam_width = 720
virtual_cam_height = 720
virtual_cam_fps = 60

### Main Program ###

# First initialise all webcams


with pyvirtualcam.Camera(width=virtual_cam_width, height=virtual_cam_height, fps=virtual_cam_fps) as virtual_cam: