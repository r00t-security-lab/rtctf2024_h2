### 猫猫密码

根据观察，以及题目提示，`不是我不想让他小写，而是真的没有小写`，可以想到摩斯密码是无法分辨大小写的。

又因为全篇只有两种重复，`喵喵？`和`喵喵喵`，于是尝试一下一个是`.`一个是`-`即可：

```python
str = ""
count = 0
output = ""
with open ('flag.txt','r',encoding='utf-8') as f:
    for line in f:
       str += line
for i in str:
    if i == "喵":
        if count == 2:
            output += '.'
            count = 0
        else:
            count += 1
    elif i == "？":
        output += '-'
        count = 0
    elif i == " ":
        output += ' '
print(output)
```
