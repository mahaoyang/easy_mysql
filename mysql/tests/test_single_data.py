#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_single_data(mysql):
    mysql.insert('test', 8)
    mysql.replace('test', 9, 'test9')
    val = [10]
    mysql.insert('test', *val)
    val = [11, 'test11']
    mysql.replace('test', *val)
    mysql.insert_ignore('test', *val)
    val = {'id': 12, 'name': 'test12'}
    mysql.insert('test', **val)
    mysql.replace('test', **val)
    mysql.insert_ignore('test', **val)
    mysql.insert('test', id=13, name='test13')
    mysql.replace('test', id=14, name='test14')
    mysql.insert_ignore('test', id=15, name='test15')
