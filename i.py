import boto3
import botocore

BUCKET_NAME = 'coderpen' # replace with your bucket name
KEY = '00000004.png' # replace with your object key

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'channel2.jpg')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise