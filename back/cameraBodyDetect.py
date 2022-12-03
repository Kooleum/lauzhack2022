__authors__ = "Alexandre Benzonana"
__version__ = "1.0"
__maintainer__ = "Alexandre Benzonana"
__email__ = "alexandre.benzonana@etu.hesge.ch"
__status__ = "Demo"

import logging, os
# from tkinter import Toplevel
# logging.disable(logging.WARNING)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import normalize

import cv2
import mediapipe as mp
import time
import threading
import time

VALIDATION_PERCENTAGE = 0.95
HAND_CERTITUDE = 0.85

# Time in s between each guess 
TIME_BETWEEN_GUESS = 0.0008

stop = False

guessPoints = [[[0, 0, 0] for i in range(52)] for j in range(30)]

def detect():   
    global stop, initialized
    videoCap = cv2.VideoCapture(0)

    
    mpBody = mp.solutions.holistic
    # mpBody.min_detection_confidence = 0.8

    mpDraw = mp.solutions.drawing_utils

    body = mpBody.Holistic()
    
    startGuess = time.time()
    globalStart = time.time()
    endGuess = 0
    maxTime = 0
    
    
    success, img = videoCap.read()

    # img = cv2.flip(img, 1)
    # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    
    cv2.imshow("image", img)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', img.shape[1], img.shape[0]) 

    while not stop:
        t = time.time()-startGuess
        print(t)
        if t > maxTime:
            maxTime = t
        startGuess=time.time()
        # print(int(tes*1000))
        
        # time.sleep(0.2)
        success, img = videoCap.read()
        # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if not success:
            continue

        # if time.time() >= startGuess + TIME_BETWEEN_GUESS:
            # startGuess = time.time()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        resBody = body.process(imgRGB)

        normHandPoints = []        
        normBodyPoints = []
        wholeNormPoints = []
        multiHand = [resBody.left_hand_landmarks, resBody.right_hand_landmarks]


        for hand in multiHand:
            if(hand):
                handPoints = []
                for i in range(21):
                    fingerPoints = [] 
                    fingerPoints.append(hand.landmark[i].x)
                    fingerPoints.append(hand.landmark[i].y)
                    fingerPoints.append(hand.landmark[i].z)
            
                    handPoints.append(fingerPoints)
                normHandPoints+=(normalize.normalizeXY(handPoints))
                
        bodyPoints = []
        if resBody.pose_landmarks:
            # print(resBody.pose_landmarks.landmark[24])
            if not (resBody.pose_landmarks.landmark[23].visibility > 0.5 and resBody.pose_landmarks.landmark[24].visibility > 0.5):
                cv2.putText(img, 'Not framed correctly', (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 6)
                cv2.putText(img, 'Not framed correctly', (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        

            mpDraw.draw_landmarks(img, resBody.pose_landmarks, mpBody.POSE_CONNECTIONS)
            
            for i in range(len(resBody.pose_landmarks.landmark)):
                if i in [0, 13, 14, 15, 16]:
                    bodyPoints.append([resBody.pose_landmarks.landmark[i].x, resBody.pose_landmarks.landmark[i].y, resBody.pose_landmarks.landmark[i].z])
                    
            normBodyPoints = normalize.normalizeXY(bodyPoints)
            
        if resBody.left_hand_landmarks:
            mpDraw.draw_landmarks(img, resBody.left_hand_landmarks, mpBody.HAND_CONNECTIONS)
            
        if resBody.right_hand_landmarks:
            mpDraw.draw_landmarks(img, resBody.right_hand_landmarks, mpBody.HAND_CONNECTIONS)

        time.sleep(0.01)

        wholeNormPoints = normHandPoints + normBodyPoints + bodyPoints
        
        if len(wholeNormPoints) == 52:           
            guessPoints.insert(0, wholeNormPoints)
            guessPoints.pop(-1)
            
        cv2.imshow("image", img)
        cv2.waitKey(1)
    print(t)
    videoCap.release()
        

threading.Thread(target=detect).start()

save = ''
while not save == 'q':
    save = input()
    
stop = True