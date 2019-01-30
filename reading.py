# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle

import pickle
import os


data = pickle.loads(open("encodings.pickle", "rb").read())
knownEncodings = data["encodings"]
knownNames = data["names"]

print(knownNames)
