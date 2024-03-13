import learm
import random
import time

import facialExpressions
import gtts
from playsound import playsound

camera_position = [1500, 500, 1364, 1325, 1888]
my_arm = learm.LeArm()

def ss_smile(my_face):
    tts = gtts.gTTS("Simon Says Smile")
    tts.save("ss_smile.mp3")
    playsound("ss_smile.mp3")
    #time.sleep(1)
    #my_face.takePicture()
    face_dict = my_face.getFaceExpression()
    if face_dict[0]['dominant_emotion'] == 'happy':
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0
def ss_angry(my_face):
    tts = gtts.gTTS("Simon Says Get Angry")
    tts.save("ss_anger.mp3")
    playsound("ss_anger.mp3")
    #time.sleep(1)
    #my_face.takePicture()
    face_dict = my_face.getFaceExpression()
    if face_dict[0]['emotion']['angry'] > 5.0:
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0
def ss_sad(my_face):
    tts = gtts.gTTS("Simon Says Look Sad")
    tts.save("ss_sad.mp3")
    playsound("ss_sad.mp3")
    #time.sleep(1)
    #my_face.takePicture()
    face_dict = my_face.getFaceExpression()
    if face_dict[0]['dominant_emotion'] == 'sad':
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0

def ss_left(my_face):
    tts = gtts.gTTS("Simon Says Move Face to Left")
    tts.save("ss_left.mp3")
    playsound("ss_left.mp3")
    #time.sleep(1)
    my_face.takePicture()
    face_dict = my_face.getFacialPos()
    if face_dict['face_1']['facial_area'][0] > 300:
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0

def ss_right(my_face):
    tts = gtts.gTTS("Simon Says Move Face to Right")
    tts.save("ss_right.mp3")
    playsound("ss_right.mp3")
    #time.sleep(1)
    my_face.takePicture()
    face_dict = my_face.getFacialPos()
    if face_dict['face_1']['facial_area'][0] < 200:
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0
    
def smile(my_face):
    tts = gtts.gTTS("Smile")
    tts.save("smile.mp3")
    playsound("smile.mp3")
    time.sleep(1)
    #my_face.takePicture()
    face_dict = my_face.getFaceExpression()
    print(face_dict)
    if not face_dict[0]['dominant_emotion'] == 'happy':
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0
def angry(my_face):
    tts = gtts.gTTS("Get Angry")
    tts.save("anger.mp3")
    playsound("anger.mp3")
    time.sleep(1)
    #my_face.takePicture()
    face_dict = my_face.getFaceExpression()
    if not face_dict[0]['emotion']['angry'] > 5.0:
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0
def sad(my_face):
    tts = gtts.gTTS("Look Sad")
    tts.save("sad.mp3")
    playsound("sad.mp3")
    #time.sleep(1)
    #my_face.takePicture()
    face_dict = my_face.getFaceExpression()
    if not face_dict[0]['dominant_emotion'] == 'sad':
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0

def left(my_face):
    tts = gtts.gTTS("Move Face to Left")
    tts.save("left.mp3")
    playsound("left.mp3")
    #time.sleep(1)
    my_face.takePicture()
    face_dict = my_face.getFacialPos()
    if not face_dict['face_1']['facial_area'][0] > 300:
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000, True)
        my_arm.moveWrist_V(500, True)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0

def right(my_face):
    tts = gtts.gTTS("Move Face to Right")
    tts.save("right.mp3")
    playsound("right.mp3")
    #time.sleep(1)
    my_face.takePicture()
    face_dict = my_face.getFacialPos()
    if not face_dict['face_1']['facial_area'][0] < 200:
        playsound("point_scored.mp3")
        my_arm.moveWrist_V(1000)
        my_arm.moveWrist_V(500)
        return 1
    else:
        playsound("fail.mp3")
        my_arm.rotateArm(1500, True)
        my_arm.rotateArm(2000, True)
        return 0

if __name__ == "__main__":
    my_face = facialExpressions.face()
    

    my_arm.moveToPosition(camera_position)
    my_arm.rotateArm(1500, True)
    my_arm.rotateArm(2000, True)
    #tts = gtts.gTTS("Hello Human, lets play some simon says, please look at my camera and maintain a neutral face until simon says otherwise")
    #tts.save("Intro.mp3")
    playsound("Intro.mp3")

    tts = gtts.gTTS("Goodjob you scored a point")
    tts.save("point_scored.mp3")

    tts = gtts.gTTS("Womp Womp No points for you!")
    tts.save("fail.mp3")
    random.seed()
    
    iteration = 0
    score = 0
    visited_node = []
    while score < 5 and iteration < 10:
        my_arm.moveToPosition(camera_position)
        identifier = random.randint(1, 10)
        if identifier in visited_node:
            continue
        else:
            visited_node.append(identifier)
        iteration +=1
        tts = gtts.gTTS("New Round! Your score is " + str(score))
        tts.save(str(score)+str(iteration)+".mp3")
        playsound(str(score)+str(iteration)+".mp3")
        if identifier == 1:
            score += ss_smile(my_face)
        elif identifier == 2:
            score += ss_angry(my_face)
        elif identifier == 3:
            score += ss_sad(my_face)
        elif identifier == 4:
            score += ss_left(my_face)
        elif identifier == 5:
            score += ss_right(my_face)
        elif identifier == 6:
            score += smile(my_face)
        elif identifier == 7:
            score += angry(my_face)
        elif identifier == 8:
            score += sad(my_face)
        elif identifier == 9:
            score += left(my_face)
        elif identifier == 10:
            score += right(my_face)
    if score >= 5:
        tts = gtts.gTTS("Great Job Human! You win!")
        tts.save("end.mp3")
        playsound("end.mp3")
    else:
        tts = gtts.gTTS("Womp Womp")
        tts.save("end2.mp3")
        playsound("end2.mp3")
