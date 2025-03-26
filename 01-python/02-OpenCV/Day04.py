'''
车辆统计 Vehicle count  [传统方法]--不具备追踪的效果


'''
import cv2 as cv
import numpy as np
min_w=90
min_h=90
# 线高
line_high = 200
# 线的偏移量
offset = 8
#车的数量
carno=0
# 存有效车的数组
cars =[]
# 求中心点
def center(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x + x1
    cy = y + y1
    return cx ,cy
# 加载视频
cap = cv.VideoCapture("video/car.mp4")

bgsubmog = cv.createBackgroundSubtractorMOG2()

# 形态学 kernel
kernel =cv.getStructuringElement(cv.MORPH_RECT,(5,5))

while True:
    ret,frame=cap.read()
    if (ret ==True):
        #灰度
        cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
       # print(frame.shape)
       # exit()
        # 高斯去噪
        blur = cv.GaussianBlur(frame,(3,3),5)
        # 去背景---《论文-MOG2》
        mask = bgsubmog.apply(blur)
        # 腐蚀     
        erode = cv.erode(mask,kernel)
        # 膨胀
        dilate =cv.dilate(erode,kernel,iterations=3)
        
        # 闭操作
        close= cv.morphologyEx(dilate,cv.MORPH_CLOSE,kernel)
        close= cv.morphologyEx(dilate,cv.MORPH_CLOSE,kernel)
        
        #轮廓
        cnts,h=cv.findContours(close,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
         #划线
        cv.line(frame,(10,line_high),(1600,line_high),(255,255,0),3)
        for(i,c) in enumerate(cnts):
           (x,y,w,h) = cv.boundingRect(c)
           cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
           #去除一些不合理的小框
           isvalue=(w>=min_w) and (h>=min_h)
           if not isvalue:
              continue
           cpoint = center(x,y,w,h)
           cars.append(cpoint)#中心点（质点）
           for (x,y) in cars:
               if((y>line_high-offset) and (y<line_high+offset)):
                   carno += 1
                   cars.remove((x,y))
                   print(carno)
        cv.putText(frame,"Cars Count:"+str(carno),(500,60),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,0),5)
        cv.imshow('video',frame)
        # cv.imshow('erode',close)

    key = cv.waitKey(1)
    if key ==27:
        break
cap.release()
cv.destroyAllWindows()