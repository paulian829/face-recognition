import cv2
import os
import numpy as np
import face_recognition as fr
import random
from config import TRAINING_IMAGES_FOLDER, TEST_DATA_FOLDER, OUTPUT_FOLDER

def identify_face(img_path,student_names):
    test_img = cv2.imread(img_path)
    faces_detected, gray_img = fr.faceDetection(test_img)


    height, width, channels = test_img.shape
    faces, faceID = fr.labels_for_training_data(TRAINING_IMAGES_FOLDER)
    face_recognizer = fr.train_classifier(faces, faceID)
    label = 'Unknown'
    for faces in faces_detected:
        (x,y,w,h) = faces
        roi_gray = gray_img[y:y+w, x:x+h]
        label, confidence = face_recognizer.predict(roi_gray)
        fr.draw_rect(test_img, faces)
        predicted_name = student_names[label]
        print(confidence)
        if confidence > 40: #If confidence more than 40 then don't print predicted face text on screen
            predicted_name = 'Unknown'
            label = 'Unknown'
        fr.put_text(test_img, predicted_name, x, y)


    # new_height = int(height/2)
    # new_width = int(width/2)
    resized_img = cv2.resize(test_img, (width, height))
    
    randomID = random.randint(1,100000)
    # Check if output folder is available if not create it
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)


    output_path = os.path.join(OUTPUT_FOLDER, str(randomID)+'.jpg')
    cv2.imwrite(output_path,resized_img)
    
    return str(randomID)+'.jpg' , label
    # cv2.imshow("face detection tutorial", resized_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows