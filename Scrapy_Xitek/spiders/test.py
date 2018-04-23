# -*- coding:utf-8 -*-
#author:zzy #data:2018/4/23 #Version:Python 3.6
import requests
url = 'http://image.xitek.com/photoiso/t653/652317_thumb.jpg'
res = requests.get(url)
with open('2.jpg','wb') as f:
    f.write(res.content)
    f.close()