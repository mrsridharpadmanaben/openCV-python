import cv2
import mediapipe as mp
import time

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prevTime = 0
curTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    '''
    print(results.multi_hand_landmarks)
    [landmark {
      x: 0.8349143862724304
      y: 0.37666282057762146
      z: -0.02165595255792141
    }]
    '''
    '''Extract Multiple Hands'''
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for idx, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h,  w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                if idx == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    ''' Showing FPS '''
    curTime = time.time()
    fps = 1 / (curTime - prevTime)
    prevTime = curTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
