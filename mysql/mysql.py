#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import pymysql
import traceback


class Mysql(object):
    def __init__(self, batch_size=10000, *args, **kwargs):
        """
            Representation of a socket with a mysql server.

            The proper way to get an instance of this class is to call
            connect().

            Establish a connection to the MySQL database. Accepts several
            arguments:

            :param host: Host where the database server is located
            :param user: Username to log in as
            :param password: Password to use.
            :param database: Database to use, None to not use a particular one.
            :param port: MySQL port to use, default is usually OK. (default: 3306)
            :param bind_address: When the client has multiple network interfaces, specify
                the interface from which to connect to the host. Argument can be
                a hostname or an IP address.
            :param unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
            :param read_timeout: The timeout for reading from the connection in seconds (default: None - no timeout)
            :param write_timeout: The timeout for writing to the connection in seconds (default: None - no timeout)
            :param charset: Charset you want to use.
            :param sql_mode: Default SQL_MODE to use.
            :param read_default_file:
                Specifies  my.cnf file to read these parameters from under the [client] section.
            :param conv:
                Conversion dictionary to use instead of the default one.
                This is used to provide custom marshalling and unmarshaling of types.
                See converters.
            :param use_unicode:
                Whether or not to default to unicode strings.
                This option defaults to true for Py3k.
            :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
            :param cursorclass: Custom cursor class to use.
            :param init_command: Initial SQL statement to run when connection is established.
            :param connect_timeout: Timeout before throwing an exception when connecting.
                (default: 10, min: 1, max: 31536000)
            :param ssl:
                A dict of arguments similar to mysql_ssl_set()'s parameters.
            :param read_default_group: Group to read from in the configuration file.
            :param compress: Not supported
            :param named_pipe: Not supported
            :param autocommit: Autocommit mode. None means use server default. (default: False)
            :param local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
            :param max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
                Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
            :param defer_connect: Don't explicitly connect on contruction - wait for connect call.
                (default: False)
            :param auth_plugin_map: A dict of plugin names to a class that processes that plugin.
                The class will take the Connection object as the argument to the constructor.
                The class needs an authenticate method taking an authentication packet as
                an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
                (if no authenticate method) for returning a string from the user. (experimental)
            :param server_public_key: SHA256 authenticaiton plugin public key value. (default: None)
            :param db: Alias for database. (for compatibility to MySQLdb)
            :param passwd: Alias for password. (for compatibility to MySQLdb)
            :param binary_prefix: Add _binary prefix on bytes and bytearray. (default: False)

            See `Connection <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_ in the
            specification.
        """
        kw = {'host': 'localhost',
              'user': 'root',
              'password': '1234',
              'charset': 'utf8mb4',
              'cursorclass': pymysql.cursors.DictCursor}
        if kwargs:
            kw.update(kwargs)
        kwargs = kw
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
            return traceback.format_exc()

    @staticmethod
    def __batch_slice(s, step):
        res = []
        quotient = len(s) // step
        if quotient:
            for index in range(quotient):
                res.append(s[index:index + step])
        else:
            res.append(s)
        return res

    def __multi_line_parser(self, table, sql, *args, **kwargs):
        res = []
        if args:
            columns_sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s'" % table
            columns = [i['COLUMN_NAME'] for i in self.execute_sql(columns_sql)]
            batch = self.__batch_slice(args, self.batch_size)
            for args in batch:
                if isinstance(args[0], dict):
                    for arg in args:
                        res.append(
                            self.__single_line_parser(sql, item=arg))
                elif isinstance(args[0], list):
                    for arg in args:
                        _columns = columns[:len(arg)]
                        res.append(
                            self.__single_line_parser(sql, item=dict(
                                zip(_columns, arg))))
                elif not isinstance(args[0], list):
                    _columns = columns[:len(args)]
                    res.append(self.__single_line_parser(sql, item=dict(
                        zip(_columns, args))))
        if kwargs:
            res.append(self.__single_line_parser(sql, item=kwargs))
        return res

    @staticmethod
    def __single_line_parser(sql, item):
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
        static = "INSERT INTO `%s` ({columns}) VALUES ({values})" % table
        sqls = self.__multi_line_parser(table, static, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def insert_ignore(self, table, *args, **kwargs):
        static = "INSERT IGNORE INTO `%s` ({columns}) VALUES ({values})" % table
        sqls = self.__multi_line_parser(table, static, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def replace(self, table, *args, **kwargs):
        static = "REPLACE INTO `%s` ({columns}) VALUES ({values})" % table
        sqls = self.__multi_line_parser(table, static, *args, **kwargs)
        for sql in sqls:
            self.execute_sql(sql)

    def delete(self, table, *args, **kwargs):
        static = "DELETE FROM `%s`  WHERE {columns} = {values}" % table
        sqls = self.__multi_line_parser(table, static, *args, **kwargs)
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

    def execute(self, sql_template, *args, **kwargs):
        sql = self.__sql_parser(sql_template, *args, **kwargs)
        self.execute_sql(sql)

    def close(self):
        return self.con.close()


if __name__ == '__main__':
    mysql = Mysql(password='rootroot', db='spider_system')
    sq = "INSERT INTO `test` (`name`) VALUES (\'{name}\')"
    # val = [{'name': 'test'}, {'name': 'test'}]
    # for i in range(100):
    #     mysql.execute(sql, *val)
    # val = [1]
    # val = [1, 'test']
    # val = [[1, 'test'], [2, 'test']]
    # val = {'id': 1, 'name': 'test1'}
    val = [{'id': 1, 'name': 'test'}, {'id': 2, 'name': 'test'}]
    # mysql.replace('test', *val)
    mysql.execute(sq, *val)
    # mysql.insert('test', *val)
    # mysql.insert_ignore('test', *val)
    # val = [1]
    # val = [[1], [2]]
    # val = {'id': 1}
    # val = [{'id': 1}, {'id': 2}]
    # mysql.delete('test', *val)
    # mysql.execute_sql("TRUNCATE TABLE test;")
