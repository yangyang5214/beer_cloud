# -*- coding: UTF-8 -*-
import json
import logging
import random
from enum import Enum

import redis
import requests

session = requests.session()

key = 'daily_tips'
key_len = 'daily_tips_len'

biying_url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx={}&n=1'

redis_pool = redis.ConnectionPool()
r = redis.Redis(connection_pool=redis_pool)


class ImageSource(Enum):
    BI_YING = 0,
    ZHI_HU = 1,
    KEEP = 2,
    MFW = 3,
    MEI_PIAN = 4,


class ImageFactory():

    def produce(self):
        pass


class KeepImage(ImageFactory):

    def produce(self):
        content = r.srandmember('keep')
        data = json.loads(content)
        return ImageResp(data['img'], data['content'], ImageSource.KEEP.name)


class ZhihuImage(ImageFactory):

    def produce(self):
        content = r.srandmember('zhihu')
        if not content:
            return
        data = json.loads(content)
        return ImageResp(data['img'], data['content'], ImageSource.ZHI_HU.name)


class MfwImage(ImageFactory):

    def produce(self):
        content = r.srandmember('mfw')
        if not content:
            return
        data = json.loads(content)
        return ImageResp(data['img'], data['content'], ImageSource.MFW.name)


class MeipianImage(ImageFactory):

    def produce(self):
        content = r.srandmember('meipian')
        if not content:
            return
        data = json.loads(content)
        return ImageResp(data['img'], data['content'], ImageSource.MFW.name)


class ImageResp:

    def __init__(self, url, msg, source):
        self.url = url if isinstance(url, list) else [url]
        self.msg = msg
        self.source = source


class BiyingImage(ImageFactory):

    def produce(self):
        url = biying_url.format(random.randint(0, 300))
        logging.info('url is {}: '.format(url))
        resp = session.get(url).json()
        img = resp['images'][0]
        url = 'https://cn.bing.com{}'.format(img['url'])
        msg = img['copyright']
        data = {
            'img': url,
            'content': msg,
        }
        r.sadd('biying', json.dumps(data))
        return ImageResp(url, msg, ImageSource.BI_YING.name)


class ImageFactory:

    def produce(self):
        pass


image_source_map = {
    'BI_YING': BiyingImage(),
    'ZHI_HU': ZhihuImage(),
    'KEEP': KeepImage(),
    'MFW': MfwImage(),
    'MEI_PIAN': MeipianImage()
}


class ImageContext:

    @staticmethod
    def factory(source):
        return image_source_map.get(source)
