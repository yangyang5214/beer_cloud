import os
import time
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib import parse as urlparse

from flask import Flask, request, jsonify
from flask_cors import CORS

pool = ThreadPoolExecutor(2)

app = Flask(__name__)
CORS(app, supports_credentials=True)

logging.basicConfig(
    level=logging.INFO,
    format=''
)


@app.route('/')
def index():
    return 'cloud api by flask'


storage_mapping = {
    'sda1': {
        'path': '/home/pi/sda1',
        'name': 'sda1',
        'url': 'http://192.168.31.158:8070',
    }
}


@app.route('/jrebel', methods=['GET'])
def jrebel_code():
    return 'https://jrebel.hexianwei.com/' + str(uuid.uuid4())


class PageHelper():

    def __init__(self, page, page_size, total, data):
        self.page = page
        self.pageSize = page_size
        self.total = total
        self.data = data


@app.route('/storages')
def storages():
    return jsonify(list(storage_mapping.values()))


@app.route('/list')
def list_file():
    prefix = request.args.get("prefix")
    storage = request.args.get("storage")
    page = int(request.args.get("page"))
    pageSize = int(request.args.get("pageSize"))
    if storage not in storage_mapping:
        return {}
    parent_path = storage_mapping.get(storage).get('path')
    if not os.path.exists(parent_path):
        return jsonify(PageHelper(page, pageSize, 0, []).__dict__)
    if not prefix:
        prefix = ''
    path = os.path.join(parent_path, prefix)

    if page <= 0:
        page = 1
    i = 0
    files = []
    total = len(os.listdir(path))
    for file in os.listdir(path):
        _path = os.path.join(path, file)
        if file.startswith('.'):
            continue
        if (page - 1) * pageSize <= i < page * pageSize:
            dir_flag = False
            date = '-'
            size = '-'
            if os.path.isdir(_path):
                dir_flag = True
            else:
                if not file.endswith('mp4'):
                    continue
            obj = {
                'name': file,
                'dirFlag': dir_flag,
                'date': date,
                'size': size,
            }
            if not dir_flag:
                img = file.replace('mp4', 'jpg')
                if not os.path.exists(os.path.join(path, img)):
                    continue
                obj['img'] = "http://192.168.31.158:8070/maomi/" + img
            files.append(obj)
        i = i + 1
    return jsonify(PageHelper(page, pageSize, total, files).__dict__)


@app.route('/del')
def del_file():
    prefix = request.args.get("prefix")
    storage = request.args.get("storage")
    if storage not in storage_mapping:
        return {}
    parent_path = storage_mapping.get(storage).get('path')
    if not prefix:
        return {}
    path = os.path.join(parent_path, prefix)

    if os.path.exists(path):
        pool.submit(run_cmd, 'rm -f {}'.format(path))
        pool.submit(run_cmd, 'rm -f {}'.format(path.replace('mp4', 'jpg')))
    return {}


@app.route('/crawler/param', methods=['POST'])
def get_url_params():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return {}
    url = url.strip()
    if not url.startswith('http'):
        url = 'http://www.fake.com?' + url
    url_parts = list(urlparse.urlparse(url))
    return dict(urlparse.parse_qsl(url_parts[4]))


@app.route('/rename')
def rename_random():
    prefix = request.args.get("prefix")
    storage = request.args.get("storage")
    parent_path = storage_mapping.get(storage).get('path')
    path = os.path.join(parent_path, prefix)
    if not os.path.exists(path):
        return {}
    final_file = prefix.split('/')[0] + '/' + str(int(time.time())) + '.' + prefix.split('.')[-1]
    cmd = 'mv {} {}'.format(path, os.path.join(parent_path, final_file))
    logging.info("rename cmd: {}".format(cmd))
    pool.submit(run_cmd, cmd)
    return {}


def run_cmd(cmd: str):
    os.system(cmd)


@app.route('/img', methods=['GET'])
def random_img():
    source = request.args.get("source")
    result = ImageContext().factory(source).produce()
    if result:
        return jsonify(result.__dict__)
    else:
        return jsonify({"msg": "服务器错误"})


@app.route('/random/bed', methods=['GET'])
def random_bed():
    img_dir = '/home/pi/sda1/public/bed'
    _url = random.choice(os.listdir(img_dir))
    base_url = 'https://www.hexianwei.com/bed/'
    return base_url + _url.strip()


if __name__ == '__main__':
    app.run(port=9001, host='0.0.0.0', debug=False, threaded=True)
