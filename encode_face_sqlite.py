# python3 encode_face_sqlite.py --dataset dataset --encodings encodings.pickle

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import sqlite3

cursor = sqlite3.connect('database.db')
print("Connected to Database")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

s = int(input("Enter The Id To Be Encoded : "))
cursor = cursor.execute("SELECT name,id from FACE_DATA")

for row in cursor:
	if(row[1] == s) :
		print("Name of Person : ", row[0])
		imagePaths = list(paths.list_files('dataset/'+str(row[1])))
print ("Operation done successfully")
cursor.close()

if os.path.exists("encodings.pickle") == False :
	knownEncodings = []
	knownNames = []
else : 
	data = pickle.loads(open("encodings.pickle", "rb").read())
	knownEncodings = data["encodings"]
	knownNames = data["names"]

for (i, imagePath) in enumerate(imagePaths):
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	encodings = face_recognition.face_encodings(rgb, boxes)

	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)

print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()