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

timer = 0
found = False
while True:
    ret, img = vid.read()

    if current_frame:
        imgS = cv2.resize(img, (0, 0), fx= 0.25, fy=0.25)
        rgb_imgS = imgS[:, :, ::-1]

        # find all the faces and face encodings in current frame of video
        facesCurFrame = face_recognition.face_locations(rgb_imgS)
        encodesCurFrame = face_recognition.face_encodings(rgb_imgS, facesCurFrame) # TODO this is what causes lag

        if not facesCurFrame: # if there are no faces restart the timer
            timer = 0
            found = False

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

            timer += 1
            if timer == 6: # if lasts for 6 seconds log
                print(f'found: {name}')
                found = True
            detected_faces.append(f'{name}')

    current_frame = not current_frame

    # display results
    for (top, right, bottom, left), name in zip(facesCurFrame, detected_faces):
        # scale face locations 5 because we shrunk the image to 1/5, 4 1/4
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        b,g,r = 0,0,0
        msgText = ''

        # create a frame with name
        if found:
            b,g,r=0,255,0 # green
            msgText = name
        elif name is not 'Unknown Student':
            b,g,r=255,0,0 # blue
            msgText = 'Detecting...'
        else:
            b,g,r=0,0,255# red
            msgText = name
        
        cv2.rectangle(img, (left, top), (right, bottom), (b,g,r), 2)
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), (b,g,r), cv2.FILLED)
        cv2.putText(img, msgText, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        vid.release()
        cv2.destroyAllWindows()          
        break
