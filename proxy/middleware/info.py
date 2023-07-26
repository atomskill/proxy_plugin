# -*- coding: utf-8 -*-

import typing as t

import flask
from proxy.utils import json_answer

from os import listdir, popen
import json

def middleware() -> t.Optional[flask.Response]:
    """ Возвращает информацию о параметрах сервиса. """
    print(flask.request.headers)
    if flask.request.method == 'INFO':
        return json_answer(getattr(flask.current_app, 'args'))

    if flask.request.method == 'GET' and 'X-Launch' in flask.request.headers:
        workdir = "/tmp/tmp"
        try:
            manifestPath = workdir + "/" + [f for f in listdir(workdir) if f.endswith(".json")][0]
        except:
            return "File not found"
        with open(manifestPath,'r') as f:
            manifest = f.read()
        execute = json.loads(manifest)['execute']
        objects = json.loads(manifest)['objects']
        print(execute)
        print(objects)

        f = open("/tmp/tmp/run.sh","w")
        script = f"#!/bin/sh\npython {execute}"
        for o in objects:
            script+= " " + o
        print(script)
        f.write(script)
        f.close()
        popen("chmod +x /tmp/tmp/run.sh")


        return popen("docker run -ti -v /tmp/tmp:/app:ro -w /app  python ./run.sh").read()

    return None
