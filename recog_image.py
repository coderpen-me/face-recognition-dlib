# python3 recog_image.py --encodings encodings.pickle --display 1

from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import sqlite3

import boto3
import botocore

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
                help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
                help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

cursor = sqlite3.connect('database.db')
print("Connected to Database")

print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

BUCKET_NAME = 'coderpen'  # replace with your bucket name
KEY1 = 'channel1.jpg'
KEY2 = 'channel2.jpg'
KEY3 = 'channel3.jpg'
s3 = boto3.resource('s3')
writer = None

while True:

    s3.Bucket(BUCKET_NAME).download_file(KEY1, 'channel_1.jpg')
    s3.Bucket(BUCKET_NAME).download_file(KEY2, 'channel_2.jpg')
    
    frame1 = cv2.imread('channel_1.jpg')
    frame2 = cv2.imread('channel_2.jpg')
    frame3 = cv2.imread('channel_3.jpg')

    KEYS = {"1": KEY1,"2":KEY2,"3" : KEY3}
    frames = [frame1, frame2, frame3]
    val = 1
    for frame in frames:
        for x, y in KEYS.items():
            if ( int(x) == val):
                Channel = y      
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=750)
        r = frame.shape[1] / float(rgb.shape[1])

        boxes = face_recognition.face_locations(rgb,model=args["detection_method"])
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],
                                                        encoding, 0.45)
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)

            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            
            if name != "Unknown":
                name = int(name)
                cursor = cursor.execute("SELECT name,id,data from FACE_DATA")

                for row in cursor:
                    if(row[1] == name) :
                        name = row[0]

            cv2.rectangle(frame, (left, top), (right, bottom),
                            (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
            cv2.putText(frame, Channel, (left, y-25), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)

        if writer is None and args["output"] is not None:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(args["output"], fourcc, 20,
                                        (frame.shape[1], frame.shape[0]), True)
            print("Writing in file")

        if writer is not None:
            writer.write(frame)

        if args["display"] > 0:
            cv2.imshow(KEYS[str(val)], frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        val = val+1
cursor.close()
if writer is not None:
    writer.release()