#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import pymysql


class Mysql(object):
    def __init__(self, batch_num=10000, *args, **kwargs):
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
        self.batch_num = batch_num

    def __execute_sql(self, sql):
        try:
            result = None
            with self.con.cursor() as cursor:
                if isinstance(sql, list):
                    # for n in range(int(len(sql) / self.batch_num) + 1):
                        for i in sql:
                            result = cursor.execute(i)
                else:
                    result = cursor.execute(sql)
            self.con.commit()
            return result
        except:
            self.con.close()

    def __columns_parser(self, table, sql, *args, **kwargs):
        res = []
        if args:
            sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % table
            columns = self.__execute_sql(sql)
            if isinstance(args[0], dict):
                for i in args:
                    res.append(self.__one_columns_parser(sql, item=i))
            elif isinstance(args[0], list):
                for i in args:
                    _columns = columns[:len(i)]
                    res.append(self.__one_columns_parser(sql, item=dict(
                        zip(_columns, i))))
            elif not isinstance(args[0], list):
                _columns = columns[:len(args)]
                res.append(self.__one_columns_parser(sql, item=dict(
                    zip(_columns, args))))
        if kwargs:
            res.append(self.__one_columns_parser(sql, item=kwargs))
        return res

    @staticmethod
    def __one_columns_parser(sql: str, item: dict):
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

    def insert(self, table, ignore=True, *args, **kwargs):
        sql = "INSERT INTO `%s` ({columns}) VALUES (values)" % table
        if ignore:
            sql = "INSERT IGNORE INTO `%s` (`name`) VALUES (values)" % table
        sql = self.__columns_parser(table=table, sql=sql, *args, **kwargs)
        self.execute(sql)

    def replace(self, table, *args, **kwargs):
        sql = "REPLACE INTO `%s` ({columns}) VALUES (values)" % table
        sql = self.__columns_parser(table=table, sql=sql, *args, **kwargs)
        self.execute(sql)

    def delete(self, table, *args, **kwargs):
        sql = "DELETE FROM `%s`  WHERE {columns} = values" % table
        sql = self.__columns_parser(table=table, sql=sql, *args, **kwargs)
        self.execute(sql)

    def __sql_parser(self, text: str, *args, **kwargs):
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
        self.__execute_sql(sql)


if __name__ == '__main__':
    mysql = Mysql(password='rootroot', db='spider_system')
    sql = "INSERT INTO `test` (`name`) VALUES (\'{name}\')"
    val = [{'name': 'test'}, {'name': 'test'}]
    # val = [['test'], ['test']]
    for i in range(100):
        mysql.execute(sql, *val)
