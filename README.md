# face-recognition-dlib
It contains program files of face recognition in video and images. Images are first transferred to cloud and then main program will download those files from cloud. After that image processing and face recognition is applied to that downloaded image. 

# Files :

1) Database.db --> This sqlite3 database file contains all the information related to pre-trained person like id, name, address.
2) drive-image.py# --> This file is uploads all clients image data to aws s3 cloud. 
3) encode_face_sqlite.py# --> This file encodes a selected person images to train the server.
4) encode_faces.py# --> This file encodes all persons available to train the server.
5) encodings.pickle# --> The file contains all trained face data.
6) recog_image.py# --> This file is server side code to download all clients images from aws s3 and apply face recognition snippet.
7) recognize_faces_video.py# --> This file is used to apply face recognition in video file.
