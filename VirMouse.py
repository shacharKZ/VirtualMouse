import cv2
import time
import handTrackingModule as htm
import autopy
import numpy as np


def main():
    pTime = 0
    wCam, hCam = 680, 480
    frameR = 77
    smoothening = 5
    plocX, plocY = 0, 0
    wScr, hScr = autopy.screen.size()
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(maxHands=1, detectionCon=0.75)
    mode = 0
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList):
            state = detector.analizeState(lmList)
            x1, y1 = lmList[8][1:]
            # x2, y2 = lmList[12][1:]

            cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (150*mode, 200, 150*mode), 2)
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            plocX, plocY = clocX, clocY

            if mode == 0 and state.count(htm.States.HALF_OPEN) and state.count(htm.States.THUMB_IN):
                mode = 1
            elif mode == 1 and state.count(htm.States.FINGER_UP) and not (state.count(htm.States.OPEN_PALM) or
                                                          state.count(htm.States.HALF_OPEN)):
                autopy.mouse.move(wScr-clocX, clocY)
                cv2.circle(img, (x1, y1), 11, (219, 172, 31), cv2.FILLED)
                if state.count(htm.States.CLICK):
                    autopy.mouse.toggle(down=True)
                    cv2.circle(img, (x1, y1), 13, (240, 70, 0), cv2.FILLED)
                else:
                    autopy.mouse.toggle(down=False)
        else:
            mode = 0




        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 3,
                    (55, 235, 52), 3)


        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
