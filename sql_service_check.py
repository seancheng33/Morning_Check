import pymssql


def main(config):
    server = config.get('sql', 'sql_server_server')  # 服务器
    user = config.get('sql', 'sql_server_username')  # 用户名
    password = config.get('sql', 'sql_server_password')  # 密码
    database = config.get('sql', 'sql_server_database')  # 数据库名

    with pymssql.connect(server, user, password, database) as conn:
        cur = conn.cursor()
        cur.callproc('dbo.MorningCheck')  # 调用存储过程
        while cur.nextset():
            # 只要有返回值，就打印出来
            print(cur.fetchall())


if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read_file(open('config.ini', 'r'))
    main(config)
