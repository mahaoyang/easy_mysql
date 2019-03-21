# masql: mysql for humans
![image](https://warehouse-camo.cmh1.psfhosted.org/1912c9df2012392febbfa09e84588bc474d9d010/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f72657175657374732e737667)

Masql is a Non-GMO mysql library for Python, safe for human consumption.

### install masql
```shell
pip install masql
```

### how to use
Behold, the power of masql:

```python
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
table_sql = "CREATE TABLE IF NOT EXISTS test(id   int PRIMARY KEY AUTO_INCREMENT,name varchar(64))charset utf8mb4;"
mysql.execute_sql(table_sql)

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
```
