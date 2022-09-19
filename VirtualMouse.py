import cv2
import time
import handTrackingModule
import autopy
import numpy as np
import uuid



def main():
    pTime = 0
    wCam, hCam = 680, 480
    frameR = 77
    smoothening = 5
    plocX, plocY = 0, 0
    wScr, hScr = autopy.screen.size()
    print(wScr, hScr)
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = handTrackingModule.handDetector(maxHands=1, detectionCon=0.7)
    while True:
        state = 0
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        counter = 0
        if len(lmList):
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            # print(x1, y1 , x2, y2)
            if lmList[8][2] < lmList[6][2]:
                state = 2
            if lmList[12][2] < lmList[10][2]:
                state += 1

            cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 100, 255), 2)
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            plocX, plocY = clocX, clocY

            # TODO

            if state >= 2:
                autopy.mouse.move(wScr-clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (77, 0, 255), cv2.FILLED)
                # if state == 3:
                #     length, img, _ = detector.findDistance(?????)
                #     if lenght < 30??:



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)


        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()





