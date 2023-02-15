import cv2
import os
import numpy as np
import face_recognition as fr

test_img = cv2.imread('test-data/elon2.jpg')
faces_detected, gray_img = fr.faceDetection(test_img)


# for (x,y,w,h) in faces_detected:
#     cv2.rectangle(test_img, (x,y), (x+w,y+h), (255,0,0), thickness=5)
    
# resized_img = cv2.resize(test_img, (1000, 700))
# cv2.imshow("face detection tutorial", resized_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows
height, width, channels = test_img.shape
# print(height, width, channels)
faces, faceID = fr.labels_for_training_data('training_images')
face_recognizer = fr.train_classifier(faces, faceID)
name={0:'Salgado', 1:'Nagal',2:'Manrique',3:'Briones'}

for faces in faces_detected:
    (x,y,w,h) = faces
    roi_gray = gray_img[y:y+w, x:x+h]
    label, confidence = face_recognizer.predict(roi_gray)
    fr.draw_rect(test_img, faces)
    predicted_name = name[label]
    # print(confidence)
    if confidence > 37: #If confidence more than 37 then don't print predicted face text on screen
        predicted_name = 'Unknown'
    fr.put_text(test_img, predicted_name, x, y)

# divide width and height by 2 and resize image

new_height = int(height/2)
new_width = int(width/2)
resized_img = cv2.resize(test_img, (new_width, new_height))
cv2.imshow("face detection tutorial", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows