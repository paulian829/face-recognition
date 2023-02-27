import cv2
import numpy as np
import os

def create_augmented_images(file_path,path,randomID):
    # Load the face image
    face = cv2.imread(file_path)

    # Create a horizontal flip of the image
    face_hflip = cv2.flip(face, 1)

    # Create a vertical flip of the image
    face_vflip = cv2.flip(face, 0)

    # Create a rotation of the image at 45 degrees
    rows, cols, _ = face.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
    face_rotated = cv2.warpAffine(face, M, (cols, rows))

    # Create a blurred version of the image
    face_blurred = cv2.GaussianBlur(face, (5, 5), 0)

    # Create a noisy version of the image
    noise = np.zeros(face.shape, np.uint8)
    cv2.randn(noise, 0, 50)
    face_noisy = cv2.add(face, noise)

    # Create a grayscale version of the image
    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    # Create a zoomed in version of the image
    zoom_scale = 1.2
    rows, cols, _ = face.shape
    M = cv2.getAffineTransform(np.float32([[0,0],[cols-1,0],[0,rows-1]]), 
                                np.float32([[cols*(1-zoom_scale)/2, rows*(1-zoom_scale)/2],
                                            [cols*(1+zoom_scale)/2, rows*(1-zoom_scale)/2],
                                            [cols/2, rows/2]]))

    # Create a sheared version of the image
    shear_angle = 30
    M = np.float32([[1, shear_angle, 0], [0, 1, 0]])

    # Create a sharpened version of the image
    kernel_sharpen = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    face_sharpened = cv2.filter2D(face, -1, kernel_sharpen)



    # output_path = os.path.join(OUTPUT_FOLDER, str(randomID)+'.jpg')
    # cv2.imwrite(output_path,resized_img)

    # Display the original and augmented images
    # cv2.imwrite('Original', face)


    cv2.imwrite(os.path.join(path,'hflip'+str(randomID)+'.jpg'), face_hflip)
    cv2.imwrite(os.path.join(path,'vflip'+str(randomID)+'.jpg'), face_vflip)
    cv2.imwrite(os.path.join(path,'blurred'+str(randomID)+'.jpg'), face_blurred)
    cv2.imwrite(os.path.join(path,'noisy'+str(randomID)+'.jpg'), face_noisy)
    cv2.imwrite(os.path.join(path,'gray'+str(randomID)+'.jpg'), face_gray)
    cv2.imwrite(os.path.join(path,'sharp'+str(randomID)+'.jpg'), face_sharpened)

    return

