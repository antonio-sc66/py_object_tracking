#  Copyright (c) 2021. Antonio Sanjurjo C.


import time
import dlib
import cv2
import argparse

WIDTH, HEIGHT = 640, 480
LIMIT_FREQ = True
FREQ = 25  # Hz

# Global vars
mouse_coords = []
new_coords = False


def mouse_event_handler(event, x, y, flags, param):
    global mouse_coords
    global new_coords

    # Store left click coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_coords = [(x, y)]

    # Record ending coordinates when left click is released
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_coords.append((x, y))
        new_coords = True


def main(input_path):
    global new_coords

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Video capture not opened. Exiting program\n")
        exit(-1)

    # Initialize the correlation tracker.
    tracker = dlib.correlation_tracker()

    # Create a named window and attach a mouse event handler
    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", mouse_event_handler)

    while True:
        t_start = time.time()
        ret, frame = cap.read()

        if frame is None:
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        # TODO resize coordinates so that processing is done with lower res than output window
        out_img = frame.copy()
        # Dlib uses RGB and CV2 uses BGR
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Start tracking when a new bounding box is defined
        if new_coords and len(mouse_coords) == 2:
            print("Initializing tracker")
            # Order the coordinates so that the first element is to the left and second element to the right
            if mouse_coords[0] > mouse_coords[1]:
                mouse_coords.reverse()

            # dlib requires the top left and bottom right, generate them if needed
            if mouse_coords[0][1] > mouse_coords[1][1]:
                top_left = (mouse_coords[0][0], mouse_coords[1][1])
                bottom_right = (mouse_coords[1][0], mouse_coords[0][1])
            else:
                top_left = mouse_coords[0]
                bottom_right = mouse_coords[1]

            cv2.rectangle(out_img, top_left, bottom_right, (0, 255, 0), 2)
            rect = dlib.rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1])
            tracker.start_track(rgb, rect)
            new_coords = False

        if not new_coords and len(mouse_coords) == 2:
            # Perform tracking
            print("Tracking...")

            tracker.update(rgb)
            track_pos = tracker.get_position()

            x1 = round(track_pos.left())
            x2 = round(track_pos.right())
            y1 = round(track_pos.top())
            y2 = round(track_pos.bottom())

            cv2.rectangle(out_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imshow("Video", out_img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("Exiting program.\n")
            # Release resources
            cap.release()
            cv2.destroyAllWindows()
            break

        if LIMIT_FREQ:
            t_end = time.time()
            t_diff = t_end - t_start
            if t_diff < 1/FREQ:
                time.sleep(1/FREQ - t_diff)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=False, type=str, default="video_samples/MOT20-02-raw.webm",
                    help="path of the input video file")
    ap.add_argument("-c", "--camera", required=False, type=int,
                    help="camera mode, enter the device number")
    args = vars(ap.parse_args())

    if args['camera'] is not None:
        main(args['camera'])
    else:
        main(args['video'])
