## Прокси-сервер

Прокси-сервис выполняет коммуникацию между системой хранения и пользователями по протоколу HTTP.


### Установка (для разработчиков)

```bash
# Склонируйте git-репощиторий.
git clone git@gitlab.com:zezyulinsv/proxy-demo.git
cd proxy-demo

# Установите виртуальное окружение.
python -m venv venv
source venv/bin/activate

# установите зависимости.
pip install flask python-magic

# установите параметры окружения для Python.
export PYTHONPATH=.
```


### Параметры запуска

```
usage: bin/proxy [-h] [--host HOST] [--port PORT] [--debug]
                 [--middleware MIDDLEWARE] [--upload-dir UPLOAD_DIR] [-v]

options:
  -h, --help               отобразить справку
  --host HOST              сетевой адрес (default: 0.0.0.0)
  --port PORT              номер порта (default: 5000)
  --debug                  отладочный режим (default: False)
  --middleware MIDDLEWARE  список middleware (разделитель запятая) (default: proxy.middleware.info.middleware)
  --upload-dir UPLOAD_DIR  директория для загружаемых файлов (default: uploads)
  -v, --version            отобразить версию
```

Пример запуска:

```bash
bin/proxy --host=129.168.0.1 --port=8080 --upload-dir=/tmp --middleware=proxy.middleware.info.middleware

# Прокси-сервер будет доступен по адресу: http://129.168.0.1:8080
# Файлы будут сохраняться в директории /tmp
# Запросы будут обрабатываться middleware "proxy.middleware.info.middleware (proxy/middlewware/info.py:middleware())"
```

### Middleware

В качестве middleware должна выступать функция, которая сможет обрабатывать запрос, выполнять его модификацию и сама
формировать ответ. Если middleware возвращает данные, то дальнейшая обработка запроса прекращается. Если необходимо
пропустить запрос далее, то middleware должен вернуть `None`.

Middleware ренистрируются Flask-приложением через метод `before_request_funcs` (смотри `proxy/app.py:Core.import_middleware()`).

Пример middleware:

```python
import flask

from proxy.utils import json_answer


def middleware():
    """ Возвращает информацию о параметрах сервиса. """
    if flask.request.method == 'INFO':
        return json_answer(getattr(flask.current_app, 'args'))
    return None
```

Пример запроса, обрабатываемый данным middleware:

```bash
curl -X INFO http://129.168.0.1:8080 | jq

# {
#   "host": "129.168.0.1",
#   "port": 8080,
#   "debug": true,
#   "middleware": "proxy.middleware.info.middleware",
#   "upload_dir": "/home/zezyulinsv/documents/proxy-demo/uploads"
# }
```
Пример запроса, который данный middleware не обрабатывает:

```bash
curl -X GET http://129.168.0.1:8080 --header "Content-Type: application/json" | jq

#[
#  {
#    "name": "test.json",
#    "size": 91,
#    "modify_time": 1689307448.5003238,
#    "content_type": "application/json"
#  }
#]
```
