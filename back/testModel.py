__authors__ = "Alexandre Benzonana"
__version__ = "1.0"
__maintainer__ = "Alexandre Benzonana"
__email__ = "alexandre.benzonana@etu.hesge.ch"
__status__ = "Demo"

import json
import logging, os
# from tkinter import Toplevel
# logging.disable(logging.WARNING)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import normalize
import neuronalNet

import cv2
import mediapipe as mp
import time
import threading
import time

VALIDATION_PERCENTAGE = 0.95
HAND_CERTITUDE = 0.85

# Time in s between each guess 
TIME_BETWEEN_FRAMES = 0.001

FRAME_BETWEEN = 10

MIN_FRAMES = 20

stop = False

model = neuronalNet.loadModel('savedModels/words.h5')

guessPoints = [[[0, 0, 0] for i in range(11)] for j in range(50)]


def detect():   
    global stop, initialized
    videoCap = cv2.VideoCapture(0)

    
    startMovement = False
    mpBody = mp.solutions.holistic
    # mpBody.min_detection_confidence = 0.8

    mpDraw = mp.solutions.drawing_utils

    body = mpBody.Holistic()
    
    startGuess = time.time()
    globalStart = time.time()
    endGuess = 0
    maxTime = 0
    
    nbFrames = 0
        
    success, img = videoCap.read()
    endMove = 0
    seuils = [0.001, 0.001, 0]

    # img = cv2.flip(img, 1)
    # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    
    cv2.imshow("image", img)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', img.shape[1], img.shape[0]) 

    lastMovingPoints = [[10, 10, 10] for i in range(4)]
    firstMovingPoints = [[10, 10, 10] for i in range(4)]

    while not stop:
        success, img = videoCap.read()

        if not success:
            continue

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        resBody = body.process(imgRGB)

                
        bodyPoints = []
        firstMovingPoints = []
        if resBody.pose_landmarks:
            # print(resBody.pose_landmarks.landmark[24])
            if not (resBody.pose_landmarks.landmark[23].visibility > 0.5 and resBody.pose_landmarks.landmark[24].visibility > 0.5):
                cv2.putText(img, 'Not framed correctly', (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 6)
                cv2.putText(img, 'Not framed correctly', (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        

            mpDraw.draw_landmarks(img, resBody.pose_landmarks, mpBody.POSE_CONNECTIONS)
            
            for i in range(len(resBody.pose_landmarks.landmark)):
                if i in [0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
                    if i in [13, 14, 15, 16]:
                        firstMovingPoints.append([resBody.pose_landmarks.landmark[i].x, resBody.pose_landmarks.landmark[i].y, resBody.pose_landmarks.landmark[i].z])
                    bodyPoints.append([resBody.pose_landmarks.landmark[i].x, resBody.pose_landmarks.landmark[i].y, resBody.pose_landmarks.landmark[i].z])
               
                    
            normBodyPoints = normalize.normalizeXY(bodyPoints)
            
        if resBody.left_hand_landmarks:
            mpDraw.draw_landmarks(img, resBody.left_hand_landmarks, mpBody.HAND_CONNECTIONS)
            
        if resBody.right_hand_landmarks:
            mpDraw.draw_landmarks(img, resBody.right_hand_landmarks, mpBody.HAND_CONNECTIONS)

        time.sleep(0.01)

        
        limits = normalize.getLimits(bodyPoints)
        
        cv2.rectangle(img, (round(limits[0][0]*img.shape[0]-10), round(limits[0][1]*img.shape[1])-10), (round(limits[1][0]*img.shape[1])+10,round(limits[1][1]*img.shape[0])+10), color=(255, 0, 0), thickness=3)
        
        if lastMovingPoints[0] != [10, 10, 10]:
            for i in range(4):
                lastMovingPoints[i][0] = abs(lastMovingPoints[i][0]-firstMovingPoints[i][0])
                lastMovingPoints[i][1] = abs(lastMovingPoints[i][1]-firstMovingPoints[i][1])
            
        if lastMovingPoints[0] < seuils and lastMovingPoints[1] < seuils and lastMovingPoints[2] < seuils and lastMovingPoints[3] < seuils:
            endMove += 1
        else:            
            if lastMovingPoints[0] != [10, 10, 10]:
                startMovement = True
            endMove = 0
        
        lastMovingPoints = firstMovingPoints
        
        
        if len(bodyPoints) == 11:     
            guessPoints.insert(0, bodyPoints)
            guessPoints.pop(-1)
            if endMove >= 5 and startMovement:
                res = neuronalNet.guess(model, guessPoints[-30:])
                endMove = 0
                print(res)
            # if (guessPoints[49][51] != [0.0, 0.0, 0.0] or endMove >= 5) and guessPoints[MIN_FRAMES][51] != [0.0, 0.0, 0.0]:
            #     print('END!!!!', endMove)
            #     word = 'hello'
            #     files = os.listdir('datas/'+word)
            #     f = open(f'datas/{word}/'+str(len(files))+'.json', 'a')
            #     f.write(json.dumps(guessPoints[-30:]))
            #     f.close()
            #     exit()
            
        cv2.imshow("image", img)
        cv2.waitKey(1)
    videoCap.release()
        

threading.Thread(target=detect).start()

save = ''
while not save == 'q':
    save = input()
    
stop = True