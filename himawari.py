#!/usr/bin/env python

# This script is based off of https://github.com/glandium/himawari-wallpaper
#
# It is reorganized to:
#
# 1. Be cron friendly (de-daemonized)
# 2. Be "distributed friendly" (state and images are saved to S3)
#

# It grabs the tiles used on http://himawari8.nict.go.jp/ to create an
# image that can be used as a wallpaper.
# The timestamp for the latest imaging available is taken from
#   http://himawari8.nict.go.jp/img/D531106/latest.json
# The corresponding tiles are available from
#   http://himawari8.nict.go.jp/img/D531106/<TILE_NUMBERS>d/550/<year>/<month>/<day>/<hh><mm><ss>_<x>_<y>.png
# where:
# - TILE_NUMBERS can be 2, 4, 8, 16 or 20. The bigger the number the more
#   detail in the tiles.
# - year, month, day, hh, mm, ss correspond to the timestamp
# - x and y are horizontal and vertical tile index, between 0 and
#   TILE_NUMBERS - 1.

# The adjustable parameters are:
# - HORIZONTAL: a range of tile numbers to use horizontally
# - VERTICAL: a range of tile numbers to use vertically
# - TIME_NUMBERS: see above.
# - SCALE: the size each tile is scaled to
# - IMAGE_PATH: the path where the aggregated image will be stored and updated.

import os
import sys, traceback
import requests
import time
import boto3
from PIL import Image, ImageDraw, ImageFont

def _read_s3_file(s3_path, key):
    return S3.Object(s3_path, key).get()["Body"].read()

def _write_s3_file(f, s3_path, key):
    S3.Object(s3_path, key).put(Body=open(f, 'rb'))

def _write_s3_string(s, s3_path, key):
    S3.Object(s3_path, key).put(Body=s)

def get_latest_image_date():
    try:
        response = session.get('%s/latest.json' % (BASE_URL))
        if response.status_code != 200:
            raise RuntimeError('HTTP 200 not received from %s' % (BASE_URL))
        
        date = response.json().get('date')
        return date
    except:
        print 'Exception while trying to find and parse latest date'
        traceback.print_exc(file=sys.stdout)

def get_latest_downloaded_image_date():
    try:
        date = _read_s3_file(IMAGE_S3_BASE_BUCKET, 'metadata/latest_date.txt')
    except:
        date = None
    return date

def timestamp_image(image, date):
    font = ImageFont.truetype('assets/CourierNew.ttf', size=40)
    draw = ImageDraw.Draw(image)
    draw.text((10,10), date, font=font)

def download_image(timestamp):
    image = Image.new('RGB', tuple(SCALE * len(n)
                                   for n in (HORIZONTAL, VERTICAL)))    

    date = timestamp.replace('-', '/').replace(' ', '/').replace(':', '')

    for x, h in enumerate(HORIZONTAL):
        for y, v in enumerate(VERTICAL):
            try:
                response = session.get('%s/%dd/550/%s_%d_%d.png' %
                                       (BASE_URL, TILE_NUMBERS, date, h, v),
                                       stream=True)
                if response.status_code != 200:
                    continue
                tile = Image.open(response.raw)    
            except:
                traceback.print_exc(file=sys.stdout)
                continue

            image.paste(tile.resize((SCALE, SCALE), Image.BILINEAR),
                        tuple(n * SCALE for n in (x, y)))

    timestamp_image(image, timestamp)
    image.save(IMAGE_TMP_PATH)

def main():
    global session
    global TILE_NUMBERS
    global BASE_URL
    global HORIZONTAL
    global VERTICAL
    global IMAGE_TMP_PATH
    global IMAGE_S3_BASE_BUCKET
    global SCALE
    global S3

    TILE_NUMBERS = 8
    HORIZONTAL = tuple(range(0, TILE_NUMBERS))
    VERTICAL = tuple(range(0, TILE_NUMBERS))
    SCALE = 350
    IMAGE = 'D531106'
    HIMAWARI = 'himawari8.nict.go.jp'
    BASE_URL = 'http://%s/img/%s' % (HIMAWARI, IMAGE)
    IMAGE_S3_BASE_BUCKET = 'earth.apawloski.com'
    S3 = boto3.resource('s3')

    session = requests.Session()

    date = get_latest_image_date()
    last_date = get_latest_downloaded_image_date()

    if date == last_date:
        print 'Should do nothing'
        sys.exit(0)
    print date
    
    last_date = date

    _write_s3_string(last_date, IMAGE_S3_BASE_BUCKET, 'metadata/latest_date.txt')

    flat_date = date.replace('-', '').replace(' ', '').replace(':', '')
    IMAGE_NAME= 'Himawari' + flat_date + '.png'
    IMAGE_PATH = './' + IMAGE_NAME
    IMAGE_TMP_PATH = '%s_%s' % os.path.splitext(IMAGE_PATH)    
    download_image(date)

    _write_s3_file(IMAGE_TMP_PATH, IMAGE_S3_BASE_BUCKET, IMAGE_NAME)    
    _write_s3_file(IMAGE_TMP_PATH, IMAGE_S3_BASE_BUCKET, 'Himawari_latest.png')

    os.rename(IMAGE_TMP_PATH, IMAGE_PATH)    
    return

if __name__ == "__main__":
    main()
