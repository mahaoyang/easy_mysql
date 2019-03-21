#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_multi_data(mysql):
    data = [[4, 'test'], [5, 'test']]
    mysql.insert('test', *data)
    mysql.replace('test', *data)
    mysql.insert_ignore('test', *data)
    data = [{'id': 6, 'name': 'test'}, {'id': 7, 'name': 'test'}]
    mysql.insert('test', *data)
    mysql.replace('test', *data)
    mysql.insert_ignore('test', *data)
