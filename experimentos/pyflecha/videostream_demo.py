from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the RaspberryPi camera should be used")
args = vars(ap.parse_args())
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    frame  = imutils.resize(frame, width=400)
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
