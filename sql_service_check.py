'''
连接sql server数据库
执行储存过程
'''

import pymssql
from Setting import Setting
setting = Setting()
server = setting.sql_server_server  # 服务器
user = setting.sql_server_username  # 用户名
password = setting.sql_server_password  # 密码
database = setting.sql_server_database  # 数据库名

with pymssql.connect(server, user, password, database) as conn:
    cur = conn.cursor()
    cur.callproc('dbo.MorningCheck')  # 调用存储过程
    while cur.nextset():
        # 只要有返回值，就打印出来
        print(cur.fetchall())
