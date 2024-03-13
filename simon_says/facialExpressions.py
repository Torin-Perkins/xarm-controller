import cv2
import matplotlib.pyplot as plt
from deepface import DeepFace
from retinaface import RetinaFace
import tensorflow as tf
import time


class face:
    def __init__(self):
        DeepFace.build_model
        RetinaFace.build_model
        
        return

    def takePicture(self):
        cam = cv2.VideoCapture(0)
        result, img = cam.read()
        if result:
            cv2.imwrite('../face_db/face.jpg', img)
        return img

    def getFaceExpression(self):
        cam = cv2.VideoCapture(0)
        result, img = cam.read()
        if result:
            cv2.imwrite('../img/face.jpg', img)
        #time.sleep(2)

        plt.imshow(img[:, :, :: -1])
        #plt.show()
        
        result = DeepFace.analyze(img_path="../img/face.jpg", actions=['emotion'])

        return result

    def getFacialPos(self):
        
        rsp = RetinaFace.detect_faces("../face_db/face.jpg")
        return rsp


if __name__ == "__main__":
    my_face = face()
    my_face.takePicture()
    print(my_face.getFacialPos())
    #print(my_face.getFaceExpression())
