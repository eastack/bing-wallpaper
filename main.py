#!/usr/bin/env python
import getopt
import sys
import os
from datetime import datetime
from json import dumps
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import requests

base_url = 'https://cn.bing.com'

width = None
height = None
date = datetime.now()

# prepare argument
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "w:h:d:", ["width=", "height=", "date="])
for opt, arg in opts:
    if opt in ['-w', '--width']:
        width = arg
    elif opt in ['-h', '--height']:
        height = arg
    elif opt in ['-d', '--date']:
        date = datetime.strptime(arg, '%Y%m%d')


def download_to_file(url, file):
    print(url)
    response = requests.get(url, stream=True)
    with open(file, 'wb') as img:
        for chunk in response.iter_content():
            img.write(chunk)


def download_wallpaper(idx):
    # https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1623641143982&pid=hp&uhd=1&uhdwidth=3840&uhdheight=2160
    response = requests.get(f'{base_url}/HPImageArchive.aspx?format=js&n=1&idx={idx}&uhd=1')
    for image in response.json()['images']:
        # init cache directory
        cache_dir = Path(Path.home() / '.cache/bing-wallpaper' / image['enddate'])
        cache_dir.mkdir(parents=True, exist_ok=True)

        # persistent metadata
        with open(cache_dir / 'metadata.json', 'w') as metadata:
            metadata.write(dumps(image))

        # download image
        # https://cn.bing.com/th?id=OHR.DragonBoatFestival2021_ZH-CN2761776128_UHD.jpg
        image_query = parse_qs(urlparse(image['url']).query)
        image_name = image_query['id'][0]
        filename, file_extension = os.path.splitext(image_name)
        download_to_file(f"{base_url}/th?id={image_name}&w={width}&h={height}&c=4", cache_dir / f'{filename}_{width}x{height}{file_extension}')


download_wallpaper((datetime.now() - date).days)
