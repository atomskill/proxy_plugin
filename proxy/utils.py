import json
import typing as t

import flask


class ComplexEncoder(json.JSONEncoder):
    """ Расширенный экземляр класса `json.JSONEncoder`. """

    def default(self, obj: t.Any) -> t.Union[str, t.Dict]:
        """
        :param obj: объект
        :return: объект, подходящий для преобразования в JSON-строку
        """
        if isinstance(obj, bytes):
            return obj.decode()
        return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)


def json_answer(
        message: t.Any,
        headers: t.Dict = None,
        mimetype: str = None,
        status_code: int = 200
) -> flask.Response:
    """ Возвращает корректно сформированные для пересылки данные в формате JSON.

    Если в строке запроса передан параметр '?pretty', то осуществляем
    форматированный вывод JSON-структуры.

    :param message: данные в любом формате
    :param headers: заголовки ответа
    :param mimetype: mime-type ответа
    :param status_code: HTTP-код ответа
    """
    result = flask.jsonify()

    # Форматированный вывод JSON-структуры, если передан параметр '?pretty'.
    indent = 2 if 'pretty' in flask.request.args else None

    # Формирование тела сообщения.
    result.data = json.dumps(message, cls=ComplexEncoder, indent=indent,
                             ensure_ascii=False)

    # Формирование кода статуса.
    result.status_code = status_code

    # Формирование заголовков.
    if headers and isinstance(headers, dict):
        result.headers.update(headers)

    # Формирование mime-type.
    if mimetype:
        result.mimetype = mimetype

    return result
