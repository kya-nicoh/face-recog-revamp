import cv2
import numpy as np
import face_recognition
import os
import pickle

stdNames = []
path = 'image'
myList = os.listdir(path)

for cl in myList:
    stdNames.append(os.path.splitext(cl)[0])
print(stdNames)

file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeStdKnown, studentIds = encodeListKnownWithIds

print('Encoding Complete')

# facial recognition
current_frame = True
vid = cv2.VideoCapture(0)

if not vid.isOpened():
    print('ERROR! No video source found...')

def faceRecog(facesCurFrame):
    encodesCurFrame = face_recognition.face_encodings(rgb_imgS, facesCurFrame)
    detected_faces = []
    for encodeFace in encodesCurFrame:
        # see if face is a match for known faces
        matches = face_recognition.compare_faces(encodeStdKnown, encodeFace)
        name = 'Unknown Student'

        # Calculate shortest distance from face
        faceDis = face_recognition.face_distance(encodeStdKnown, encodeFace)

        # checks if face are a match
        isMatch = np.argmin(faceDis)
        if matches[isMatch]:
            name = stdNames[isMatch]

        return name

timer = 0
msgText = 'Welcome'
while True:
    ret, img = vid.read()

    # if current_frame:
    imgS = cv2.resize(img, (0, 0), fx= 0.25, fy=0.25)
    rgb_imgS = imgS[:, :, ::-1]

    # find all the faces and face encodings in current frame of video
    facesCurFrame = face_recognition.face_locations(rgb_imgS)


    # TODO if there are no faces and 3 seconds elapsed reset
    if not facesCurFrame: # if there are no faces restart the timer 
        timer = 0
        msgText = 'Welcome'

    for (top, right, bottom, left) in facesCurFrame:
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        b,g,r = 0,255,0
        
        timer += 1 # BUG WHEN ONLY 1's reset DONT KNOW WHATS CAUSING IT YET.
        # TODO MAKE USE OF FUNCTIONS
        print(timer)
        if timer == 20:
            cv2.putText(img, 'LOADING', (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
            cv2.waitKey(1)
            msgText = faceRecog(facesCurFrame)
            
        cv2.rectangle(img, (left, top), (right, bottom), (b,g,r), 2)
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), (b,g,r), cv2.FILLED)
        cv2.putText(img, msgText, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

    # current_frame = not current_frame

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        vid.release()
        cv2.destroyAllWindows()          
        break
