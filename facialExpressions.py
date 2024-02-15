import cv2
import matplotlib.pyplot as plt
from deepface import DeepFace
import time

class face:
    def __init__(self):
        return
    def getFaceExpression(self):
        cam = cv2.VideoCapture(0)
        result, img = cam.read()
        if result:
            cv2.imwrite('img/face.jpg', img)
        time.sleep(2)

        plt.imshow(img[:, :, : : -1])
        plt.show()

        result = DeepFace.analyze(img, actions=['emotion'])


        return result

if __name__ == "__main__":
    my_face = face()
    print(my_face.getFaceExpression())