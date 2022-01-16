import cv2
import numpy as np
framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)

mycolors = [[32,130,65,96,197,255],
            [0,74,156,69,202,255]]

mycolorvalues = [[51,255,51],
                 [51,255,255]]

mypoints = [] #[x,y,colorId]

def findcolor(img,mycolors,mycolorvalues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints=[]
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgresult,(x,y),10,mycolorvalues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]),mask)
    return newpoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>500:
            #cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y


def drawOnCanvas(mypoints,mycolorvalues):
    for point in mypoints:
        cv2.circle(imgresult, (point[0], point[1]), 10, mycolorvalues[point[2]], cv2.FILLED)


while True:
    success,img = cap.read()
    imgresult = img.copy()
    newpoints = findcolor(img,mycolors,mycolorvalues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawOnCanvas(mypoints,mycolorvalues )

    cv2.imshow("Result",imgresult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break