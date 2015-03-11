# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

fileNames = ['0-9m', '0-9p', '0-9s', '1-7z']

for fileName in fileNames :
    col = fileName[len(fileNames) - 1]
    if col in 'msp' :
        l, r = 0, 9
    else :
        l, r = 1, 7
    img = cv2.imread('image\\' + fileName + '.jpg')
    print type(img), type(img[0]), type(img[0][0]), img[0][0], img.shape
    h, w = img.shape[0:2]
    for i in range(l, r + 1) :
        curL = w / (r - l + 1) * (i - l)
        print '%d%s.jpg' % (i, col)
        cv2.imwrite('image\\%d%s.jpg' % (i, col), img[0 : h, curL : curL + w / (r - l + 1) - 1])
