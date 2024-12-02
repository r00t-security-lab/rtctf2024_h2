### 听说你学懂了base64

首先根据题目描述，用010打开png，得到一串：

```
i think u need this : 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/=
```

可知这是替换后的新表。

然后打开密文后，发现他是一行一行的base64，与我们常见的一整段，只有末尾有等号的base64不太一样。这里实际上是利用了base64等号其实是因为不足六位而补0得到的，由于在解密的时候末尾的填充会被省略去，所以实际上我们可以在填充的位置隐藏我们想要的信息，事实上flag也被隐藏在这里。

利用脚本提取，注意，因为一行最多能藏两个等号的信息，所以行数很多，其实也给了我们一个提醒，如果以后遇到了行数很多的base64，大概率就是这样隐藏的

```python
d = '''

'''  # 将加密后的内容放到这个多行字符串中

base64chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/="
e = d.splitlines()  # 将输入字符串按行分割
binstr = ""  # 初始化二进制字符串为空

# 遍历每行内容
for i in e :
    if i.find("==")>0:
        temp=bin((base64chars.find(i[-3])&15))[2:]
    #取倒数第3个字符，在base64找到对应的索引数（就是编码数），取低4位，再转换为二进制字符
        binstr=binstr + "0"*(4-len(temp))+temp #二进制字符补高位0后，连接字符到binstr
    elif i.find("=")>0:
        temp=bin((base64chars.find(i[-2])&3))[2:] #取倒数第2个字符，在base64找到对应的索引数（就是编码数），取低2位，再转换为二进制字符
        binstr=binstr + "0"*(2-len(temp))+temp #二进制字符补高位0后，连接字符到binstr
str_ = bytearray()
for i in range(0, len(binstr), 8):
    if i + 8 <= len(binstr):
        index = int(binstr[i:i + 8], 2)  # 每 8 位转换为索引值
        if 0 <= index < 256:  # 确保索引值在有效范围内
            str_.append(index)  # 追加字节数据到 bytearray

print(str_.decode('utf-8'))  
```
