#!/usr/bin/env python
from urllib.parse import urlparse, parse_qs

import requests
import time
import os
from pathlib import Path

nc = int(time.time() * 1000)
base_url = 'https://cn.bing.com'
cache_dir = Path.home() / Path('.cache/bing-wallpaper')

# 获取今日图片
# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1623641143982&pid=hp&uhd=1&uhdwidth=3840&uhdheight=2160
response = requests.get(f'{base_url}/HPImageArchive.aspx?format=js&n=1&nc={nc}&uhd=1')
image = response.json()['images'][0]

# 下载图片
# https://cn.bing.com/th?id=OHR.DragonBoatFestival2021_ZH-CN2761776128_UHD.jpg
image_query = parse_qs(urlparse(image['url']).query)
image_name = image_query['id'][0]
image_full_path = cache_dir / image_name
if not image_full_path.exists():
    response = requests.get(f"{base_url}/th?id={image_name}", stream=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    with open(image_full_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

# 设置为壁纸
wallpaper = Path.home() / Path('pictures/wallpaper.png')
os.unlink(wallpaper)
os.symlink(image_full_path, wallpaper)
os.system(Path.home() / Path('.fehbg'))
