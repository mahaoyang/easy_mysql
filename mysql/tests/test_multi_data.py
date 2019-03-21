#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_multi_data(mysql):
    val = [[4, 'test'], [5, 'test']]
    mysql.insert('test', *val)
    mysql.replace('test', *val)
    mysql.insert_ignore('test', *val)
    val = [{'id': 6, 'name': 'test'}, {'id': 7, 'name': 'test'}]
    mysql.insert('test', *val)
    mysql.replace('test', *val)
    mysql.insert_ignore('test', *val)
