#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from mysql.mysql import Mysql
from mysql.tests.test_execute import test_execute
from mysql.tests.test_single_data import test_single_data
from mysql.tests.test_multi_data import test_multi_data


def test_main():
    mysql = Mysql(host='localhost', user='root', password='rootroot',
                  db='default')
    mysql.execute_sql("CREATE SCHEMA IF NOT EXISTS `default`;")
    mysql.execute_sql(
        "CREATE TABLE IF NOT EXISTS test(id   int PRIMARY KEY AUTO_INCREMENT,name varchar(64))charset utf8mb4;")
    test_execute(mysql)
    test_single_data(mysql)
    test_multi_data(mysql)
    mysql.close()


if __name__ == '__main__':
    test_main()

from mysql import Mysql

"""
get connection
"""
mysql = Mysql(host='localhost', user='root', password='rootroot', db='default')

"""
creat test table
and execute the raw sql
"""
mysql.execute_sql("CREATE SCHEMA IF NOT EXISTS `default`;")
mysql.execute_sql(
    "CREATE TABLE IF NOT EXISTS test(id   int PRIMARY KEY AUTO_INCREMENT,name varchar(64))charset utf8mb4;")

"""
table : test
column : id , name
"""

data = [{'id': 6, 'name': 'test'},
        {'id': 7, 'name': 'test'}]  # [{k0:v0,k1:v1},{k0:v0,k1:v1}]
mysql.insert('test', *data)
mysql.replace('test', *data)
mysql.insert_ignore('test', *data)

mysql.insert_ignore('test', {'id': 6, 'name': 'test'}, {'id': 7,
                                                        'name': 'test'})  # is equal to "mysql.insert_ignore('test', *data)"

data = [[4, 'test'], [5, 'test']]  # [[c0,c1],[c0,c1]]
mysql.insert('test', *data)
mysql.replace('test', *data)
mysql.insert_ignore('test', *data)

mysql.close()
