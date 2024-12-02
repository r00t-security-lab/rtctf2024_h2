python写脚本跑可以，用yakit不断发包也可以这里还是推荐写脚本

f12查看网络，点击抽一发，发现抽卡请求是/draw，并且会返回一个json，其中的type表示抽出来的是否是flag

```python
import requests
import json
while True:
    rep=requests.get('http://124.222.157.100:33106/draw').json()
    if rep['type']=='normal':
        pass
    else:
        print(rep)
        break
```

