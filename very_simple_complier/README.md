# Introduction

一个 <b>充满了bug</b> 的 <b>超简单小型</b> 编译器。

代码借鉴了这里

http://justjavac.com/python/2012/04/13/one-day-write-language-in-python.html

# Instruction

`python gao.py FILE`

对文件进行操作

`python gao.py`

可 interactively 操作

# Example

	def Fib(x) {
		if ((x == 0) + (x == 1)) {
			return 1
		} else {
			return Fib(x - 1) + Fib(x - 2)
		}
	}
	i = 0
	while (i <= 10) {
		print Fib(i)
		i = i + 1
	}

会输出前 11 个斐波那契数。

	