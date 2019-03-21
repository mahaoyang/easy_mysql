#!/usr/bin/python3
# -*- encoding: utf-8 -*-


def test_execute(mysql):
    sq = "REPLACE INTO `test` (`id`,`name`) dataUES ({id},\'{name}\')"
    data = {'id': 1, 'name': 'test1'}
    mysql.execute(sq, **data)
    sq = "REPLACE INTO `test` (`id`,`name`) dataUES (%s,\'%s\')"
    mysql.execute(sq, 2, 'test2')
    data = [3, 'test3']
    mysql.execute(sq, *data)
