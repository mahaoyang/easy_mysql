#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_single_data(mysql):
    mysql.insert('test', 8)
    mysql.replace('test', 9, 'test9')
    data = [10]
    mysql.insert('test', *data)
    data = [11, 'test11']
    mysql.replace('test', *data)
    mysql.insert_ignore('test', *data)
    data = {'id': 12, 'name': 'test12'}
    mysql.insert('test', **data)
    mysql.replace('test', **data)
    mysql.insert_ignore('test', **data)
    mysql.insert('test', id=13, name='test13')
    mysql.replace('test', id=14, name='test14')
    mysql.insert_ignore('test', id=15, name='test15')
