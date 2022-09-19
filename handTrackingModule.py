import cv2
import mediapipe as mp
import time
from enum import Enum


class States(Enum):
    OPEN_PALM = 1
    HALF_OPEN = 2
    FINGER_UP = 3
    CLICK = 4
    THUMB_IN = 5

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.75, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils



    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 33), cv2.FILLED)

        return lmList


    def analizeState(self, lmList):
        if not lmList:
            return
        res = []

        states_open_fingers = []
        states_open_fingers.append(lmList[4][2] <= lmList[5][2])
        for tip in range(8, 21, 4):
            states_open_fingers.append(lmList[tip][2] < lmList[tip-2][2])

        states_between_fingers = []
        states_between_fingers.append(abs(lmList[4][1]-lmList[5][1]) > abs(lmList[3][1]-lmList[5][1]))
        for tip in range(8, 17, 4):
            states_between_fingers.append(abs(lmList[tip][1]-lmList[tip+4][1]) > abs(lmList[tip-2][1]-lmList[tip+2][1]))

        if lmList[4][2] > lmList[9][2] and (lmList[5][1] < lmList[4][1] < lmList[17][1] or
                                            lmList[5][1] > lmList[4][1] > lmList[17][1]):
            res.append(States.THUMB_IN)

        if abs(lmList[4][1] - lmList[6][1]) < abs(lmList[7][1] - lmList[6][1]):
            res.append(States.CLICK)

        if states_open_fingers[1]:
            res.append(States.FINGER_UP)

        if states_open_fingers.count(1) == 5 and states_between_fingers.count(1) == 4:
            res.append(States.OPEN_PALM)
        elif states_open_fingers[1:].count(1) == 4:
            res.append(States.HALF_OPEN)

        return res

# while True:
#     success, img = cap.read()
#
#     cTime = time.time()
#     fps = 1/(cTime-pTime)
#     pTime = cTime
#
#     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
#                  (255, 0, 255), 3)
#
#     cv2.imshow('Image', img)
#     cv2.waitKey(1)


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        detector.analizeState(lmList)
        # if len(lmList):
        #     print(lmList[8])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

