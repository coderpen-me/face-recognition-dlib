import boto3
import cv2


# Create an S3 client
s3 = boto3.client('s3')

filename = 'channel1.jpg'
bucket_name = 'coderpen'

cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    cv2.imwrite('channel1.jpg', frame)
    cv2.imshow('img', frame)
    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(filename, bucket_name, filename)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
