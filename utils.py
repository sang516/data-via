import pymysql


def get_mysql_connection():
    return pymysql.connect(host='localhost', port=3306,
                           user='guest', password='Guest.618',
                           database='data_viz', charset='utf8mb4')
