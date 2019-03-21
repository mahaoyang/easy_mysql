#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_single_data(mysql):
    mysql.truncate('test')
    mysql.insert('test', 1)
    mysql.replace('test', 1, 'test1')
    val = [2]
    mysql.insert('test', *val)
    val = [2, 'test2']
    mysql.replace('test', *val)
    mysql.insert_ignore('test', *val)
    val = {'id': 3, 'name': 'test3'}
    mysql.insert('test', **val)
    mysql.replace('test', **val)
    mysql.insert_ignore('test', **val)
    mysql.insert('test', id=4, name='test4')
    mysql.replace('test', id=4, name='test4')
    mysql.insert_ignore('test', id=4, name='test4')
