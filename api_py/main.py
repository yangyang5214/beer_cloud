import os
import time

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return 'cloud api by flask'


storage_mapping = {
    'sda1': {
        'path': '/home/pi/sda1',
        'name': 'sda1',
        'url': 'http://192.168.31.158:8070',
    },
    'local': {
        'path': '/Users/beer',
        'name': 'local',
        'url': 'http://192.168.31.158:8070',
    }
}


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
                stat = os.stat(_path)
                size = stat.st_size
                date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(stat.st_ctime)))
            obj = {
                'name': file,
                'dirFlag': dir_flag,
                'date': date,
                'size': size,
            }
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
    os.remove(path)
    return {}


if __name__ == '__main__':
    app.run(port=9001, host='0.0.0.0')
