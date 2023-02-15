import cv2
import os
import numpy as np
import face_recognition as fr
import random


def identify_face(img_path,student_names):
    test_img = cv2.imread(img_path)
    faces_detected, gray_img = fr.faceDetection(test_img)


    height, width, channels = test_img.shape
    faces, faceID = fr.labels_for_training_data('training_images')
    face_recognizer = fr.train_classifier(faces, faceID)

    for faces in faces_detected:
        (x,y,w,h) = faces
        roi_gray = gray_img[y:y+w, x:x+h]
        label, confidence = face_recognizer.predict(roi_gray)
        fr.draw_rect(test_img, faces)
        predicted_name = student_names[label]
        if confidence > 37: #If confidence more than 37 then don't print predicted face text on screen
            predicted_name = 'Unknown'
        fr.put_text(test_img, predicted_name, x, y)


    new_height = int(height/2)
    new_width = int(width/2)
    resized_img = cv2.resize(test_img, (new_width, new_height))
    
    randomID = random.randint(1,100000)
    output_path = os.path.join('output', str(randomID)+'.jpg')
    cv2.imwrite(output_path,resized_img)
    
    return output_path
    # cv2.imshow("face detection tutorial", resized_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows