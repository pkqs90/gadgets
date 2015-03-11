#coding=utf-8

import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Solution :
    def findNumOfCards(self, pts) :
        # 把散点分成几个聚合的块，返回牌数
        tot = len(pts)
        vis = [0] * tot
        ret = []
        for i in range(tot) :
            if vis[i] == 1 :
                continue
            _x, _y, cnt = 0, 0, 0
            for j in range(tot) :
                # 把同一个牌型的牌相近的都压到一块儿
                if (abs(pts[j][0] - pts[i][0]) + abs(pts[j][1] - pts[i][1]) <= 30) and vis[j] == 0 :
                    _x += pts[j][0]
                    _y += pts[j][1]
                    cnt += 1
                    vis[j] = 1
            _x = (int) (_x / (float (cnt)))
            _y = (int) (_y / (float (cnt)))
            ret.append((_x, _y))
        return ret

    def Detect(self, originalName, templateName, flag) :
        # flag == 0 返回每张牌的匹配度
        # flag == 1 返回每张牌匹配了多少次
        originalImage = cv2.imread(originalName)
        templateImage = cv2.imread('image\\' + templateName)

        scale = originalImage.shape[0] / (float (templateImage.shape[0]))
        templateImage = cv2.resize(templateImage, None, fx = scale, fy = scale)
        self.cardWidth = templateImage.shape[1]

        res = cv2.matchTemplate(originalImage, templateImage, cv2.TM_CCOEFF_NORMED)

        threshold = cv2.minMaxLoc(res)[1] - 0.03
        loc = np.where(res >= threshold)
        pts = self.findNumOfCards(zip(*loc[::-1]))

        if flag == 0 :
            return [threshold, pts]
        else :
            # 把找到的牌输出到屏幕上用红框框出来
            # h, w = templateImage.shape[0 : 2]
            # for pt in pts:
            #     cv2.rectangle(originalImage, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            # cv2.imshow('...', originalImage)
            # cv2.waitKey(0)
            return len(pts)

    def findCard(self, fileName) :
        _names = ['%dm' % x for x in range(1, 10)]
        _names += ['%dp' % x for x in range(1, 10)]
        _names += ['%ds' % x for x in range(1, 10)]
        _names += ['%dz' % x for x in range(1, 8)]

        dic = {}
        for _name in _names :
            ret = self.Detect(fileName, _name + '.jpg', 0)
            # if ret[0] > 0.60 :
            dic[_name] = ret
            # print _name, ret

        # 找到按匹配程度从大到小找到出现了哪些牌，一旦有冲突就 break
        dic = sorted(dic.items(), key = lambda x: x[1][0], reverse = True)
        pts, ret = [], []

        for i in dic :
            flag = True
            for j in i[1][1] :
                for k in pts :
                    # 冲突定义为 "横插" 进一张牌
                    if abs(j[0] - k[0]) + abs(j[1] - k[1]) <= self.cardWidth * 6 / 10 :
                        flag = False
                        break
                if not flag :
                    break
            if flag :
                pts += i[1][1]
                ret += [i[0]]

        return ret

    def Solve(self, fileName) :

        # 返回在牌中的牌型
        _names = self.findCard(fileName)

        ret = []
        for _name in _names :
            num = self.Detect(fileName, _name + '.jpg', 1)
            ret.append((_name, num))
        return sorted(ret, cmp = lambda a, b: cmp(a[0][1] + a[0][0], b[0][1] + b[0][0]) )

    def __init__(self) :

        # 实际图中牌宽
        self.cardWidth = 0

if __name__ == '__main__' :
    if len(sys.argv) > 1 :
        fileName = sys.argv[1]
        a = Solution()
        print a.Solve(fileName)
    else :
        print 'File name?'
