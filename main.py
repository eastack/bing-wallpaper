#!/usr/bin/env python
import getopt
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests

base_url = 'https://cn.bing.com'

width = None
height = None
today = datetime.now()

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "w:h:d:", ["width=", "height=", "date="])
for opt, arg in opts:
    if opt in ['-w', '--height']:
        width = arg
    elif opt in ['-h', '--width']:
        height = arg
    elif opt in ['-d', '--date']:
        today = datetime.strptime(arg, '%Y%M%d')

timestamp, _ = divmod(today.timestamp(), 1 / 1000)

# 获取今日图片
# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1623641143982&pid=hp&uhd=1&uhdwidth=3840&uhdheight=2160
print(int(timestamp))
print(f'{base_url}/HPImageArchive.aspx?format=js&n=1&nc={int(timestamp)}&uhd=1')
exit()
response = requests.get(f'{base_url}/HPImageArchive.aspx?format=js&n=1&nc={int(timestamp)}&uhd=1')
image = response.json()['images'][0]

# 下载图片
# https://cn.bing.com/th?id=OHR.DragonBoatFestival2021_ZH-CN2761776128_UHD.jpg
image_query = parse_qs(urlparse(image['url']).query)
image_name = image_query['id'][0]
response = requests.get(f"{base_url}/th?id={image_name}&w={width}&h={height}", stream=True)
for chunk in response.iter_content():
    sys.stdout.buffer.write(chunk)
sys.stdout.buffer.close()
