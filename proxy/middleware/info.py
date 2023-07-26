# -*- coding: utf-8 -*-

import typing as t

import flask

from proxy.utils import json_answer


def middleware() -> t.Optional[flask.Response]:
    """ Возвращает информацию о параметрах сервиса. """
    if flask.request.method == 'INFO':
        return json_answer(getattr(flask.current_app, 'args'))
    return None
