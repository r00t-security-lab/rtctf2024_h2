import requests
import json

rep=requests.get('http://124.222.157.100:32789/draw').json()

while rep['type']=='normal':
    rep=requests.get('http://124.222.157.100:32789/draw').json()
    print(rep)

print(rep)