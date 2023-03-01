import cv2
import face_recognition
import pickle
import os


# importing the images
folderPath = 'image'
folderPathList = os.listdir(folderPath)
imgList = []
studentID = []

for path in folderPathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentID.append(os.path.splitext(path)[0])

# encodings
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodeListKnown = findEncodings(imgList)

# save to a pickle file
encodeListKnownWithIds = [encodeListKnown, studentID]

file = open('EncodeFile.p', 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()