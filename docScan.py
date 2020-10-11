# Document Scan
## Mitchell Ciupak
## 20201011

import cv2
import numpy as np

#CONST
WIDTH_IMG = 640
HEIGHT_IMG = 480

# Start Cam
cap = cv2.VideoCapture(0)
cap.set(3,WIDTH_IMG)
cap.set(4,HEIGHT_IMG)
cap.set(10,150) #brightness

def preProcessing(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray,(5,5),1)
    img_canny = cv2.Canny(img_blur,200,200) #TODO may adjust

    kernel = np.ones((5,5))
    img_dial = cv2.dilate(img_canny,kernel,iterations=2)

    return cv2.erode(img_dial,kernel, iterations=1)

def detectContours(img):
    bestContour = np.array([])
    maxArea = 0

    contours, hierarchy = cv2.findContours(img,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(contours)
        if area > 5000: #reduce noise and add drawing
            cv2.drawContours(img_contour, cnt, contourIdx=-1, color=(255, 0, 0), thickness=3)
            peri = cv2.arcLength(curve=cnt,closed=True)
            approxCorners = cv2.approxPolyDP(curve=cnt,epsilon=0.02*peri,closed=True)
            approxNumCorners = len(approxCorners)

            if area > maxArea and approxNumCorners == 4:
                bestContour = approxCorners
                maxArea = area
    return bestContour

while True:
    isValid, img = cap.read()
    img = cv2.resize(img,(WIDTH_IMG,HEIGHT_IMG))
    img_contour = img.copy()

    img_thresh = preProcessing(img)
    bestContour = detectContours(img_thresh)
    getWarp(img,bestContour)

    cv2.imshow("Output", img_contour)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break