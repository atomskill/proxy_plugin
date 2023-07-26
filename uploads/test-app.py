#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv


def main() -> None:
    data = ""

    # Сохранение содержимого указанных файлов
    # в переменную data.
    file_list = argv[1:]
    for file in file_list:
        with open(file) as f:
            data += f.read()

    # Вывод содержимого файлов.
    print(data)


if __name__ == '__main__':
    exit(main())
