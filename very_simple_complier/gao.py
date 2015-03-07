#coding=utf-8

import re
import sys

class SyntaxException(Exception) :
    pass

def fenCi(_str) :
    ret = []
    i = 0
    tot = len(_str)
    while (i < tot) :
        if (re.match(r'[.\d]', _str[i]) != None) :
            cur = ''
            while (i < tot and re.match(r'[.\d]', _str[i]) != None) :
                cur += _str[i]
                i += 1
            try :
                if ('.' in cur) :
                    cur = float(cur)
                else :
                    cur = int(cur)
            except :
                raise SyntaxException('%s is not a number' % cur)
            ret.append(cur)
        elif (re.match(r'[a-zA-Z_]', _str[i]) != None) :
            cur = ''
            while (i < tot and re.match(r'[a-zA-Z0-9_]', _str[i]) != None) :
                cur += _str[i]
                i += 1
            ret.append(cur)
        elif (_str[i] in '+-*/(){};,<>=') :
            if (i + 1 < tot and _str[i : i + 2] == '==') : ret.append('=='); i += 2
            elif (i + 1 < tot and _str[i : i + 2] == '>=') : ret.append('>='); i += 2
            elif (i + 1 < tot and _str[i : i + 2] == '<=') : ret.append('<='); i += 2
            else : ret.append(_str[i]); i += 1
        elif (_str[i] in ' \t\n') :
            i += 1
        else :
            raise SyntaxException('WTF is \'%s\' ?' % _str[i])
    return ret


class Method :
    pass

class Environment :

    def __init__(self, parent = None) :
        self.hash = {}
        self.parent = parent
        self.end = False

    def setValue(self, key, val) :
        self.hash[key] = val

    def getValue(self, key) :
        if (key in self.hash) :
            return self.hash[key]
        else :
            if (self.parent == None) :
                raise SyntaxException('%s is not declared.' % key)
            else :
                return self.parent.getValue(key)

class Parser :

    def __init__(self) :
        self.env = Environment()
        self.word = []
        self.p = 0

    def hasNext(self, pos = 0) :
        return self.p + pos < self.tot

    def getNext(self, pos = 0) :
        return self.word[self.p + pos]

    def notNext(self, ch) :
        if (self.hasNext() == False or self.getNext() != ch) :
            return True
        return False

    def isNext(self, ch, pos = 0) :
        if (self.hasNext(pos) == True and self.getNext(pos) == ch) :
            return True
        return False

    def isSymbol(self, _str) :
        if (type(_str) != str) : return False
        if (len(_str) == 0) : return False
        if (re.match(r'[a-zA-Z_]', _str[0]) != None) :
            return True
        return False

    def passCurrentModule(self) :
        cnt = 1
        while (self.hasNext()) :
            if (self.getNext() == '{') : cnt += 1;
            if (self.getNext() == '}') : cnt -= 1;
            if (cnt == 0) :
                break
            self.p += 1
        if (cnt != 0) :
            raise SyntaxException('Missing \'}\'.')



    def run(self, _str) :                           # It all begins here.
        self.p = len(self.word)
        self.word += fenCi(_str)
        self.tot = len(self.word)
        if (self.hasNext()) :
            return self.expList()

    def expList(self) :
        while (self.hasNext()) :
            if (self.getNext() == ';') :
                self.p += 1
            elif (self.getNext() == '}') :          # This is important. Jump out of current module.
                break
            else :
                ret = self.exp()
            if (self.env.end == True) :
                break
        return ret

    def exp(self) :
        if (self.hasNext()) :
            if (type(self.getNext()) == str and self.getNext() in ';}') :
                return
        if (self.hasNext(1)) :
            if (self.getNext(1) == '=') :
                return self.passVal()
            elif (self.getNext() == 'if') :
                return self.condition()
            elif (self.getNext() == 'while') :
                return self.loop()
            elif (self.getNext() == 'def') :
                return self.method()
            elif (self.getNext() == 'return') :
                return self._return()
            elif (self.getNext() == 'print') :
                return self._print()
        return self.lTop()

    def passVal(self) :                             # Note that it is able to deal with consecutive '='s
        _str = self.getNext()
        if (self.isSymbol(_str) == False) :
            raise SyntaxException('At position %d, WTF is \'%s\' ?' % (self.p, _str))
        self.p += 2
        ret = self.exp()
        self.env.setValue(_str, ret)
        return ret;

    def condition(self) :                           # if (lTop) {expList} [ else {expList} ]
                                                    # Note that 'lTop' and 'expList' can't be empty
        self.p += 1
        if (self.notNext('(')) : raise SyntaxException('Missing \'(\' after if')
        self.p += 1
        val = self.lTop()
        if (self.notNext(')')) : raise SyntaxException('Missing \')\' after if')
        self.p += 1
        if (self.notNext('{')) : raise SyntaxException('Missing \'{\' after if')
        self.p += 1
        if (val != 0) :
            ret = self.expList()
        else :
            ret = None
            self.passCurrentModule()
        if (self.notNext('}')) : raise SyntaxException('Missing \'}\' after if')
        self.p += 1

        if (self.isNext('else')) :
            self.p += 1
            if (self.notNext('{')) : raise SyntaxException('Missing \'{\' after else')
            self.p += 1
            if (val != 0) :
                self.passCurrentModule()
            else :
                ret = self.expList()
            if (self.notNext('}')) : raise SyntaxException('Missing \'}\' after else')
            self.p += 1
        return ret

    def loop(self) :                                # while (lTop) {expList}
                                                    # Note that 'lTop' and 'expList' can't be empty
        self.p += 1
        pTemp = self.p
        while True :
            if (self.notNext('(')) : raise SyntaxException('Missing \'(\' after while')
            self.p += 1
            val = self.lTop()
            if (self.notNext(')')) : raise SyntaxException('Missing \')\' after while')
            self.p += 1
            if (self.notNext('{')) : raise SyntaxException('Missing \'{\' after while')
            self.p += 1
            if (val != 0) :
                ret = self.expList()
            else :
                self.passCurrentModule()
            if (self.notNext('}')) : raise SyntaxException('Missing \'}\' after if')
            self.p += 1
            if (val != 0) :
                self.p = pTemp
            else :
                break
        return ret


    def method(self) :
        self.p += 1
        func = Method()
        if (self.hasNext() == False or self.isSymbol(self.getNext()) == False) : raise SyntaxException('Incorrect method name: %s.' % func.funcName)
        func.funcName = self.getNext()
        # if (func.funcName in self.env.hash) : raise SyntaxException('%s Method already defined.' % func.funcName)
        # Bugs exist when running interactively .. How to solve .. ??
        self.p += 1
        if (self.notNext('(')) : raise SyntaxException('Missing \'(\' after method name %s' % func.funcName)
        self.p += 1
        func.funcArgs = self.getFuncArgs(func.funcName)
        if (self.notNext(')')) : raise SyntaxException('Missing \')\' after method name %s' % func.funcName)
        self.p += 1
        if (self.notNext('{')) : raise SyntaxException('Missing \'{\' after method name %s' % func.funcName)
        self.p += 1
        func.p = self.p
        self.env.setValue(func.funcName, func)
        self.passCurrentModule()
        if (self.notNext('}')) : raise SyntaxException('Missing \'}\' after method name %s' % func.funcName)
        self.p += 1
        return func

    def getFuncArgs(self, funcName) :
        ret = []
        if (self.isNext(')')) :
            return ret
        while (self.hasNext()) :
            ret.append(self.getNext())
            self.p += 1
            if (self.isNext(',')) : self.p += 1
            elif (self.isNext(')')) : break
            else : raise SyntaxException('Wrong grammer for method %s' % funcName)
        for _str in ret :
            if (self.isSymbol(_str) == False) :
                raise SyntaxException('Wrong argument for method %s' % funcName)
        return ret

    def getCallArgs(self, funcName) :
        ret = []
        if (self.isNext(')')) :
            return ret
        while (self.hasNext()) :
            ret.append(self.lTop())
            if (self.isNext(',')) : self.p += 1
            elif (self.isNext(')')) : break
            else : raise SyntaxException('Wrong grammer for method %s' % funcName)
        return ret

    def pushEnv(self, env, func) :
        self.env = env
        self.p = func.p
    def popEnv(self) :
        if (self.env.parent == None) :
            raise SyntaxException('Incorrect while conducting \'Return\'.')
        self.env = self.env.parent
        self.p = self.env.p

    def methodCall(self, func, args) :
        if (len(args) != len(func.funcArgs)) :
            raise SyntaxException('Wrong number of arguments passed in method %s' % func.funcName)
        self.env.p = self.p
        env = Environment(self.env)
        for (a, b) in zip(func.funcArgs, args) :
            env.setValue(a, b)
            # print (a, b)
        self.pushEnv(env, func)
        ret = self.expList()
        self.popEnv()
        return ret

    def _return(self) :
        self.p += 1
        ret = self.lTop()
        self.env.end = True
        return ret

    def _print(self) :
        self.p += 1
        ret = self.lTop()
        print ret
        return ret



    def lTop(self) :                                # Dealing with arithmitic expressions
        return self.l3()

    def l0(self) :
        # print ('You are at L0! Position: %d %s' % (self.p, self.getNext()))
        ret = self.getNext()
        if (ret == '(') :
            self.p += 1                             # (
            ret = self.lTop()                       # ...
            self.p += 1                             # )
            return ret
        elif (type(ret) == int or type(ret) == float) :
            self.p += 1
            return ret
        elif (ret == '-' and self.hasNext(1) and (type(self.getNext(1)) == int or type(self.getNext(1)) == float)) :
            ret = -self.getNext(1)
            self.p += 2
            return ret
        elif (self.isSymbol(ret)) :                 # Is a symbol -> Method name
            if (isinstance(self.env.getValue(ret), Method) and self.isNext('(', 1)) :
                func = self.env.getValue(ret)
                self.p += 2
                args = self.getCallArgs(func.funcName)
                if (self.notNext(')')) : raise SyntaxException('Missing \')\' after method %s' % func.funcName)
                self.p += 1
                return self.methodCall(func, args)
            else :                                  # Is a symbol -> Variable name
                self.p += 1
                ret = self.env.getValue(ret)
                return ret
        else :
            raise SyntaxException('At position %d, WTF is \'%s\' ?' % (self.p, ret))

    def l1(self) :
        # print ('You are at L1! Position: %d' % self.p)
        if (self.p == self.tot) :
            return None
        ret = self.l0()
        while (self.p < self.tot) :
            curOp = self.getNext()
            if (curOp in '*/') :
                self.p += 1
                val = self.l0()
                if (val == None) :
                    raise SyntaxException('Error on level L1, incorrect operand')
                if (curOp == '*') : ret *= val
                if (curOp == '/') :
                    if (val == 0) :
                        raise SyntaxException('Error on level L1, divisor is 0')
                    ret /= val
            else :
                break
        return ret

    def l2(self) :
        # print ('You are at L2! Position: %d' % self.p)
        if (self.p == self.tot) :
            return None
        ret = self.l1()
        while (self.p < self.tot) :
            curOp = self.getNext()
            if (curOp in '+-') :
                self.p += 1
                val = self.l1()
                if (val == None) :
                    raise SyntaxException('Error on level L2, incorrect operand')
                if (curOp == '+') : ret += val
                if (curOp == '-') : ret -= val
            else :
                break
        return ret

    def l3(self) :
        # print ('You are at L3! Position: %d' % self.p)
        val1 = self.l2()
        if (self.p < self.tot) :
            if (self.getNext() == '<=' or self.getNext() == '>=' or self.getNext() == '==' or
                self.getNext() == '<' or self.getNext() == '>') :
                curOp = self.getNext()
                self.p += 1
                val2 = self.l2()
                if (val2 == None) :
                    raise SyntaxException('Error on level L3, incorrect operand')
                if (val1 <= val2 and curOp == '<=') : return 1
                if (val1 >= val2 and curOp == '>=') : return 1
                if (val1 == val2 and curOp == '==') : return 1
                if (val1 < val2 and curOp == '<') : return 1
                if (val1 > val2 and curOp == '>') : return 1
                return 0
            """else :
                raise SyntaxException('Error on level L3, incorrect operation')"""
        return val1


if __name__ == '__main__' :
    sol = Parser()
    if len(sys.argv) > 1 :
        fileObject = open(sys.argv[1], 'r')
        content = fileObject.read()
        sol.run(content)
    else :
        try :
            while True :
                try :
                    _str = raw_input('==> ')
                    if (_str == '--help') :
                        print '并没有什么可以 help 的'.decode('utf-8').encode('gbk')
                    else :
                        print sol.run(_str)
                except SyntaxException as err:
                    print 'Syntax error: ', err
        except (EOFError, KeyboardInterrupt) :
            print 'Goodbye.'

