import cv2
import time
import os
import handTrackingModule as hd

def printNum(img, n):
    cv2.putText(img, str(int(n)), (600, 400), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 77), 3)

tipIds = [(4, 5), (8,6), (12,10), (16,14), (20,18)]

def main():
    pTime = 0
    wCam, hCam = 680, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = hd.handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        counter = 0
        if len(lmList):
            for id in tipIds:
                if lmList[id[0]][2] < lmList[id[1]][2]:
                    counter += 1

        printNum(img, counter)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)


        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()





