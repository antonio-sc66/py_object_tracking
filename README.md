# Py Object Tracking

This project provides an example of how to use OpenCV and dlib to perform object tracking with Python.

The code doesn't perform check to ensure that the tracking doesn't get confused with other objects
of to handle occlusions, in this case the tracker will keep reporting the last position.


## Usage
Download a video sample to perform tracking and place it under video_samples. Video examples can be found in https://motchallenge.net/data/MOT20/.

Download ex:
```
wget https://motchallenge.net/sequenceVideos/MOT20-01-raw.webm
mv MOT20-01-raw.webm video_samples
```

Execute the code with Python3:
```
python3 main.py
```

**Left click and hold** on the first point of the bounding box and **drag** until you select the whole object, **release
the left mouse button** and the tracking will start.

Press **'Q'** to **exit** the program.

## Licence
This project is licenced under **GPL-3.0**, check **LICENCE** to get a copy of the licence. 


#### TODO
 - Add argparse to allow camera mode or video input