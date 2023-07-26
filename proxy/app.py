# -*- coding: utf-8 -*-

import argparse
import logging
import typing as t
from importlib import import_module
from os import listdir, stat
from os.path import abspath, exists
from re import match
from stat import S_ISDIR

import flask
from magic import Magic

from .utils import json_answer

logging.basicConfig(format='')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Core:
    def __init__(self, args: argparse.Namespace):
        self.app = flask.Flask(__name__)
        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule(
            '/upload', view_func=self.upload, methods=['PUT'])
        self.app.add_url_rule('/download/<path:path>', view_func=self.download)

        # Параметры запуска.
        self.app.args = args
        self.host = args.host
        self.port = args.port
        self.debug = args.debug
        self.upload_dir = args.upload_dir
        self.middleware = args.middleware.replace(' ', '').split(',')

        # Регистрация middleware.
        self.import_middleware()

    def run(self) -> None:
        log.info(f' * Upload dir: {self.upload_dir}')
        self.app.run(host=self.host, port=self.port,
                     debug=self.debug, threaded=True)

    def import_middleware(self) -> None:
        """ Регистрация middleware. """
        # Регистрируем внешние middleware.
        middleware_list = []
        for middleware in self.middleware:
            result = match(r'(.*)\.(.*)', middleware)
            if result:
                module_name, func_name = result.groups()
                module = import_module(module_name)
                middleware_list.append(getattr(module, func_name))
        self.app.before_request_funcs = {None: middleware_list}

    def index(self) -> t.Union[flask.Response, str]:
        """ Возвращает список объектов. """
        path = abspath(self.upload_dir)
        magic = Magic(mime=True, uncompress=True)

        files = []
        for filename in listdir(path):
            filepath = f'{path}/{filename}'
            filestat = stat(filepath)
            if not S_ISDIR(filestat.st_mode):
                files.append({
                    'name': filename,
                    'size': filestat.st_size,
                    'modify_time': filestat.st_mtime,
                    'content_type': magic.from_file(filepath)
                })

        if flask.request.is_json:
            return json_answer(files)
        return flask.render_template('default.html', files=files)

    def upload(self) -> flask.Response:
        """ Загружает объект на сервер. """

        def gen(chunk_size: int = 8192) -> str:
            while True:
                chunk = flask.request.stream.read(chunk_size)
                if len(chunk) == 0:
                    break
                yield chunk

        buffer = bytes()
        for i in gen():
            buffer += i

        filename = flask.request.headers.get('X-Name')
        path = abspath(self.upload_dir)

        f = open(f'{path}/{filename}', mode='wb')
        f.write(buffer)
        f.close()

        return flask.Response("upload success")

    def download(self, path: str) -> flask.Response:
        """ Отдаёт содержимое объекта. """
        path = f'{abspath(self.upload_dir)}/{path}'

        if not exists(path):
            flask.abort(404)

        try:
            return flask.send_file(path)
        except Exception as error:
            flask.abort(flask.Response(str(error), 503))


def run(args: argparse.Namespace):
    """ Запуск веб-сервера. """
    server = Core(args)
    server.run()
