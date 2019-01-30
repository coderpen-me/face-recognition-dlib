import cloudinary
import cloudinary.uploader
import cloudinary.api
import cv2

cloudinary.config( 
  cloud_name = "coderpen", 
  api_key = "279718938876221", 
  api_secret = "NdYDcw6kJIvt2_YXFRQj-vXXWIU" 
)

cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    cv2.imwrite('channel1.jpg', frame)    
    cv2.imshow('img',frame)

    cloudinary.uploader.upload("channel1.jpg", public_id="channel1", overwrite=True)
    
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()