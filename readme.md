# Automatic Webcam Selector

This program will automatically decide which webcam to use based on gaze detection. It is powered by the GazeTracking python module (https://github.com/antoinelame/GazeTracking).

### Why use this?
If you have a multi-monitor setup, you may look disengaged in meetings when looking at monitors that don't have your webcam. If you have spare webcams lying around, this program allows you to put a webcam on each of your monitors, and it will then decide which one to display based on the gaze detection (calculating which webcam you are most likely to be looking at).

### Reliability
I've made this as a fun project, and from my limited testing it works quite well - despite the virtual camera being awful quality. Basically, I wouldn't recommend using it in client meetings...

### Setup
1. You will first want to install OBS (https://obsproject.com/), this uses the OBS virtual camera to start.
2. Launch OBS, and click the "Start Virtual Camera" button, then click to stop the virtual camera and close the OBS app. This has now created a virtual camera that this program can use to pipe video into.
3. Configure the settings for this program (see below)
4. Run main.py and see magic happen. You will have to play whack-a-mole with installing requirements because I haven't included a requirements file - I should probably do that...


### Configuration
To start configuring the script, open the main.py file. There are various options to configure.

`webcam_ids` - This is a list of device ids for your webcams. Most likely starting from 0. The more cameras you have, the more likely the program is to run slower or require more compute resources. The time complexity will exponentially increase as more cameras are added (sorry, this isn't built for efficiency).

`measurement_range` - This determines how many measurements are factored into deciding which webcamera to display at any given time. The larger this number, the more accurate the switching is likely to be, but it will also be slower. As a guide, if this is set to around 5, your cameras will be switching all over the place, but if it is set to 120, the script will probably be factoring in measurements that are 1 second late (not good).

`cooldown_Seconds` - This is one protection against the program randomly flickering between cameras. Each time a camera is switched out for another one, the script will not switch cameras again until a cooldown has run for this amount of seconds.

`favourite_webcam_id` - This allows you to pick a single webcam to be the favourite (you will probably want this to be the one you are most likely to be looking at).

`favourite_webcam_weighting` - This will let you set a multiplier weighting for the above favourite webcam. Setting this value to 1, will do nothing, setting it to 2 will double the weightings of the favourite camera, making it more likely to select that camera over other cameras. This is only a rough weighting, if your favourite camera has zero measurements of you looking at it, the weighting will mean nothing. If you have a small measurement range, this weighting also won't have much of an impact. Fine tune it as needed, or just set it to 1 to keep things simple.

`virtual_cam_width` - Self explanatory

`virtual_cam_height` - Self explanatory

`virtual_cam_fps` - Self explanatory. I'm not entirely sure if this actually does anything...