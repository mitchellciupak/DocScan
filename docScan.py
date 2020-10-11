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
        area = cv2.contourArea(cnt)
        if area > 5000: #reduce noise and add drawing
            cv2.drawContours(img_contour, cnt, contourIdx=-1, color=(255, 0, 0), thickness=3)
            peri = cv2.arcLength(curve=cnt,closed=True)
            approxCorners = cv2.approxPolyDP(curve=cnt,epsilon=0.02*peri,closed=True)
            approxNumCorners = len(approxCorners)

            if area > maxArea and approxNumCorners == 4:
                bestContour = approxCorners
                maxArea = area
    return bestContour

def orderWarp(pts):
    pts = pts.reshape((4,2))
    ptsUpdated = np.zeros((4,1,2),np.int32)

    add = pts.sum(1)
    diff = np.diff(pts, axis=1)

    ptsUpdated[0] = pts[np.argmin(add)]
    ptsUpdated[1] = pts[np.argmin(diff)]
    ptsUpdated[2] = pts[np.argmax(diff)]
    ptsUpdated[3] = pts[np.argmax(add)]

    return ptsUpdated

def detectWarp(img,contour):
    contour = orderWarp(contour)

    pts1 = np.float32(contour)
    pts2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOut = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))

    return cv2.resize(imgOut,(WIDTH_IMG,HEIGHT_IMG))


while True:
    isValid, img = cap.read()
    img = cv2.resize(img,(WIDTH_IMG,HEIGHT_IMG))
    img_contour = img.copy()

    img_thresh = preProcessing(img)
    bestContour = detectContours(img_thresh)
    img_warped = detectWarp(img,bestContour)

    cv2.imshow("Output", img_warped)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break