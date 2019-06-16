#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pylab import *
import cv2
import pytesseract
from PIL import Image


im1 = Image.open('20181119131712.png')
img = cv2.imread('20181119131712.png')#打开图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#转换成灰度图
ret, binary = cv2.threshold(gray, 150,255, cv2.THRESH_BINARY_INV)#二值化

element1_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))#腐蚀函数 对横线进行腐蚀
element1_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))#腐蚀函数 对竖线进行腐蚀
element1_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))#直接对4x4进行腐蚀
element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))#膨胀函数 ()中的是膨胀的范围
erosion1 = cv2.erode(binary, element1_1, iterations = 1)
erosion2 = cv2.erode(binary, element1_2, iterations = 1)

binary = array(binary)
x = erosion2.shape[0]#宽
y = erosion2.shape[1]#长
#消除存在的表格线
for i in range(x):
    for j in range(y):
        if(erosion2[i,j] == 255 or erosion1[i,j] == 255 ):
            binary[i , j] = 0
            binary[i , j] = 0

dilation2 = cv2.dilate(binary, element2, iterations = 1)#对10x10进行膨胀

im = array(img)
x1 = 0
x2 = 0
x3 = 0
x4 = 0
temp1 = 0
temp2 = 0


#dilation2 = array(dilation2)
i = 0
while(i<x):
    j = 0
    while(j < y):
        if (dilation2[i,j] == 255):
            x1 = i#记录初始点
            x2 = j
            k = j + 2
            for w in range(i,x):
                if (dilation2[w, k] == 0):#找到末端点的纵坐标
                    x3 = w
                    break
            for w in range(j,y):#找到末端点的横坐标
                sum = 0
                for k in range(i,x3):
                    sum += dilation2[k,w]
                    if(dilation2[k,w] == 255):
                        x4 = w
                        break
                if (sum == 0):
                    break
            for w in range(j,0,-1):#倒回去重新寻找初始点的目标 因为膨胀不均匀可能导致同个目标被分成多个框
                sum = 0
                for k in range(i,x3):
                    sum += dilation2[k,w]
                    if(dilation2[k,w] == 255):
                        x2 = w
                        break
                if (sum == 0):
                    break
            if((x3-x1)*(x4-x2)<100):#防止过小的图片进入(过滤)
                # 标出此区域后 就把该区域变成白色 以免再次检测
                for w in range(x1 - 5, x3 + 5):
                    for k in range(x2 - 5, x4 + 5):
                        dilation2[w, k] = 0
                j = x4 + 1
                continue
            im2 = im1.crop((x2-20,x1,x4,x3))#切割图片
            if (temp1 in range(x1,x3) and temp2 in range(x2,x4)):#寻找对应关键字下面的文字
                imshow(im2)
                show()
            text2 = u'名称'#进行转码
            text1 = pytesseract.image_to_string(im2, lang='chi_sim')
            print text1
            if(text2 in text1):#检查关键字
                temp1 = x3+35#用一个列表来做
                temp2 = (x2+x4)/2
                #imshow(im2)
                #show()
            '''
            plot((x2, x4), (x1, x1))  # 前面两个是要连的横坐标 后面两个是要连的纵坐标
            plot((x4, x4), (x1, x3))
            plot((x2, x4), (x3, x3))
            plot((x2, x2), (x1, x3))
           '''
            #标出此区域后 就把该区域变成白色 以免再次检测
            for w in range(x1-5,x3+5):
                for k in range(x2-5,x4+5):
                    dilation2[w,k] = 0
            j = x4 + 1
        else:
            if(j == y - 1):
                #if(x3>i):
                    #i = x3 + 1
                #else:
                i = i+1
            j = j + 1


imshow(im)
show()