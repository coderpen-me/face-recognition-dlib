import boto3
import cv2

s3 = boto3.client('s3')

filename = 'channel1.jpg'
bucket_name = 'coderpen'

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    cv2.imwrite('channel1.jpg', frame)
    cv2.imshow('img', frame)
    s3.upload_file(filename, bucket_name, filename)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
