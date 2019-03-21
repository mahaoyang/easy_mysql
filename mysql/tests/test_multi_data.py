#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_multi_data(mysql):
    mysql.truncate('test')
    val = [[1, 'test'], [2, 'test']]
    mysql.insert('test', *val)
    mysql.replace('test', *val)
    mysql.insert_ignore('test', *val)

    val = [{'id': 3, 'name': 'test'}, {'id': 4, 'name': 'test'}]
    mysql.insert('test', *val)
    mysql.replace('test', *val)
    mysql.insert_ignore('test', *val)
