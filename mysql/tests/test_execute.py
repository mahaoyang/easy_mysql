#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_execute(mysql):
    mysql.truncate('test')
    sq = "REPLACE INTO `test` (`id`,`name`) VALUES ({id},\'{name}\')"
    val = {'id': 1, 'name': 'test1'}
    mysql.execute(sq, **val)
    sq = "REPLACE INTO `test` (`id`,`name`) VALUES (%s,\'%s\')"
    mysql.execute(sq, 2, 'test2')
    val = [3, 'test3']
    mysql.execute(sq, *val)
