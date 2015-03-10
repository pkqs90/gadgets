import copy

# 1-9M = 0-8
# 1-9S = 9-17
# 1-9P = 18-26
# DNXBZFB = 27-33

class ErrorException(Exception) :
    pass

class Solution :
    def Dfs(self, st, flag, sz) :

        # for i in range(6) :
        #     print i, ',', self.val[i]
        # print self.cur, sz

        if sz == 2 :
            for i in range(34) :
                if self.val[i] == 2 :
                    self.cur.append([i] * 2)
                    self.ret.append(copy.deepcopy(self.cur))
                    self.cur.pop()
            return
        if flag == 0 :
            self.Dfs(0, 1, sz)
            for i in range(st, 34) :
                if self.val[i] >= 3 :
                    self.val[i] -= 3
                    self.cur.append([i] * 3)
                    self.Dfs(i, 0, sz - 3)
                    self.cur.pop()
                    self.val[i] += 3
        else :
            for i in range(st, 27) :
                if i % 9 == 0 or i % 9 == 8 :
                    continue
                if self.val[i - 1] and self.val[i] and self.val[i + 1] :
                    for j in range(i - 1, i + 2) :
                        self.val[j] -= 1
                    self.cur.append([j for j in range(i - 1, i + 2)])
                    self.Dfs(i, 1, sz - 3)
                    self.cur.pop()
                    for j in range(i - 1, i + 2) :
                        self.val[j] += 1


    def __init__(self, arr) :
        if len(arr) % 3 != 2 or len(arr) <= 0 or len(arr) > 14 :
            raise ErrorException('Wrong number of cards')
        self.val = [0 for i in range(34)]
        self.cur = []
        self.ret = []
        for i in arr :
            if type(i) != int or i < 0 or i > 34 :
                raise ErrorException('Wrong input of cards: %s' % i)
            self.val[i] += 1
        self.Dfs(0, 0, len(arr))
        # for i in range(34) :
        #     print i, ',', self.val[i]

arr = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]
# arr = [1, 2, 3, 4, 4]
a = Solution(arr)
for i in a.ret :
    print i
