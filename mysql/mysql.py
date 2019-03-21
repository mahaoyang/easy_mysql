#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import pymysql
import traceback


class Mysql(object):
    def __init__(self, batch_size=10000, *args, **kwargs):
        kw = {'host': 'localhost',
              'user': 'root',
              'password': '1234',
              'charset': 'utf8mb4',
              'cursorclass': pymysql.cursors.DictCursor}
        if kwargs:
            kw.update(kwargs)
        kwargs = kw
        if len(args) and len(args) < 5:
            self.con = pymysql.connect(*args, **kwargs)
        elif kwargs:
            self.con = pymysql.connect(*args, **kwargs)
        self.batch_size = batch_size

    @staticmethod
    def __is_select(sql):
        return True if 'SELECT' in sql.upper() else False

    def execute_sql(self, sql):
        try:
            result = None
            select_flag = False
            with self.con.cursor() as cursor:
                if isinstance(sql, list):
                    for i in sql:
                        select_flag = self.__is_select(i)
                        result = cursor.execute(i)
                else:
                    select_flag = self.__is_select(sql)
                    result = cursor.execute(sql)
            self.con.commit()
            if select_flag:
                return cursor.fetchall()
            return result
        except Exception as E:
            self.con.close()
            return traceback.format_exc()

    @staticmethod
    def __slice(s, step):
        res = []
        quotient = len(s) // step
        if quotient:
            for index in range(quotient):
                res.append(s[index:index + step])
        else:
            res.append(s)
        return res

    def __columns_parser(self, table, sql, *args, **kwargs):
        res = []
        if args:
            columns_sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s'" % table
            columns = [i['COLUMN_NAME'] for i in self.execute_sql(columns_sql)]
            batch = self.__slice(args, self.batch_size)
            for args in batch:
                if isinstance(args[0], dict):
                    for arg in args:
                        res.append(self.__one_columns_parser(sql, item=arg))
                elif isinstance(args[0], list):
                    for arg in args:
                        _columns = columns[:len(arg)]
                        res.append(self.__one_columns_parser(sql, item=dict(
                            zip(_columns, arg))))
                elif not isinstance(args[0], list):
                    _columns = columns[:len(args)]
                    res.append(self.__one_columns_parser(sql, item=dict(
                        zip(_columns, args))))
        if kwargs:
            res.append(self.__one_columns_parser(sql, item=kwargs))
        return res

    @staticmethod
    def __one_columns_parser(sql, item):
        columns = ''
        values = ''
        for key, value in item.items():
            columns += '`%s`,' % key
            if isinstance(value, int):
                values += '%s,' % value
            else:
                values += '\'%s\',' % value
        columns = columns.strip(',')
        values = values.strip(',')
        sql = sql.format(columns=columns, values=values)
        return sql

    def insert(self, table, *args, **kwargs):
        sql = "INSERT INTO `%s` ({columns}) VALUES ({values})" % table
        sqls = self.__columns_parser(table, sql, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def insert_ignore(self, table, *args, **kwargs):
        sql = "INSERT IGNORE INTO `%s` ({columns}) VALUES ({values})" % table
        sqls = self.__columns_parser(table, sql, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def replace(self, table, *args, **kwargs):
        sql = "REPLACE INTO `%s` ({columns}) VALUES ({values})" % table
        sqls = self.__columns_parser(table, sql, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def delete(self, table, *args, **kwargs):
        sql = "DELETE FROM `%s`  WHERE {columns} = {values}" % table
        sqls = self.__columns_parser(table, sql, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def __sql_parser(self, text, *args, **kwargs):
        res = []
        if args:
            if isinstance(args[0], dict) and '{' in text:
                for i in args:
                    res.append(text.format(**i))
            elif not isinstance(args[0], list) and '%s' in text:
                res.append(text % args)
            elif isinstance(args[0], list) and '%s' in text:
                for i in args:
                    res.append(text % tuple(i))
            return res
        if kwargs:
            res.append(text.format(**kwargs))
            return res

    def execute(self, text, *args, **kwargs):
        sql = self.__sql_parser(text, *args, **kwargs)
        self.execute_sql(sql)


if __name__ == '__main__':
    mysql = Mysql(password='rootroot', db='spider_system')
    sql = "INSERT INTO `test` (`name`) VALUES (\'{name}\')"
    # val = [{'name': 'test'}, {'name': 'test'}]
    # for i in range(100):
    #     mysql.execute(sql, *val)
    # val = [1]
    # val = [1, 'test']
    # val = [[1, 'test'], [2, 'test']]
    # val = {'id': 1, 'name': 'test1'}
    val = [{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'test'}]
    # mysql.replace('test', *val)
    mysql.execute(sql, *val)
    # mysql.insert('test', *val)
    # mysql.insert_ignore('test', *val)
    # val = [1]
    # val = [[1], [2]]
    # val = {'id': 1}
    # val = [{'id': 1}, {'id': 2}]
    # mysql.delete('test', *val)
    # mysql.execute_sql("TRUNCATE TABLE test;")
