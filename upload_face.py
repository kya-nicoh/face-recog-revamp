# upload image with face / or with video
# find face
# save as 216x216 image

import cv2
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def find_face_image(uploaded_image):
    img = cv2.imread(uploaded_image)

    while True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
        
        cv2.imshow('img', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # change name later
            cv2.imwrite('Image'+'.jpg', face)
            image = Image.open('Image'+'.jpg')
            resized_image = image.resize((216,216))
            resized_image.save('Image'+'.jpg')
            break
        
    cv2.destroyAllWindows()

def find_face_cam():
    vid = cv2.VideoCapture(0)

    while True:
        ret, img = vid.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            face = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
        
        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # change name later
            cv2.imwrite('Cam'+'.jpg', face)
            image = Image.open('Cam'+'.jpg')
            resized_image = image.resize((216,216))
            resized_image.save('Cam'+'.jpg')
            break
        
    vid.release()
    cv2.destroyAllWindows()

find_face_cam()
# find_face_image('ANTONIO.jpg')