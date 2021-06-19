import random

import pymysql
from flask import Flask, redirect, request
from flask_cors import CORS

from utils import get_mysql_connection

app = Flask(__name__)
CORS(app)


@app.route('/')
def show_index():
    # 将请求重定向到static目录下的index.html
    return redirect('/static/index.html')


# API - Application Programming Interface - 应用程序编程接口
# 网络API（网络数据接口）- 请求这个URL就可以获得对应的数据（通常是JSON格式）
@app.route('/api/general_data')
def get_general_data():
    names = ('GMV', '销售额', '实际销售额', '客单价')
    divsors = (10000, 10000, 10000, 1)
    units = ('万元', '万元', '万元', '元')
    values = [0] * 4
    conn = get_mysql_connection()
    try:
        sql_queries = [
            'select sum(orderAmount) from tb_order',
            'select sum(payment) from tb_order',
            'select sum(payment) from tb_order where chargeback="否"',
            'select sum(payment) / count(distinct userID) from tb_order where chargeback="否"'
        ]
        with conn.cursor() as cursor:
            for i, query in enumerate(sql_queries):
                cursor.execute(query)
                values[i] = round(float(cursor.fetchone()[0]) / divsors[i], 2)
    except pymysql.MySQLError as err:
        print(err)
    finally:
        conn.close()
    results = [{'name': names[i], 'unit': units[i], 'value': values[i]} for i in range(4)]
    return {'results': results}


@app.route('/api/gmv_by_month')
def get_gmv_by_month():
    conn = get_mysql_connection()
    months, gmvs = [], []
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('select month(orderTime) as month, sum(orderAmount) as gmv from tb_order group by month')
            row_dict = cursor.fetchone()
            while row_dict:
                months.append(f'{row_dict["month"]}月')
                gmvs.append(round(float(row_dict['gmv']) / 10000, 2))
                row_dict = cursor.fetchone()
    except pymysql.MySQLError as err:
        print(err)
    finally:
        conn.close()
    return {'x': months, 'y': gmvs}


@app.route('/api/channel_data')
def get_channel_data():
    conn = get_mysql_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('select chanelID as name, count(distinct userID) as value from tb_order group by chanelID order by value desc')
            results = cursor.fetchall()
    except pymysql.MySQLError as err:
        print(err)
    finally:
        conn.close()
    return {'results': results}


@app.route('/api/sales_data')
def get_sales_data():
    y1_data = [random.randrange(10, 41) for _ in range(6)]
    y2_data = [random.randrange(20, 51) for _ in range(6)]
    y3_data = [random.randrange(30, 41) for _ in range(6)]
    y4_data = [random.randrange(20, 31) for _ in range(6)]
    return {'y1': y1_data, 'y2': y2_data, 'y3': y3_data, 'y4': y4_data}


@app.route('/api/stock_data')
def get_stock_data():
    # 获取查询参数（URL参数，跟在URL之后?后面的参数）
    start = request.args.get('start', '2020-1-1')
    end = request.args.get('end', '2020-12-31')
    conn = pymysql.connect(host='localhost', port=3306,
                           user='guest', password='Guest.618',
                           database='stock', charset='utf8mb4')
    x_data, y_data = [], []
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                'select trade_date, open_price, close_price, low_price, high_price '
                'from tb_baba_stock where trade_date between %s and %s',
                (start, end)
            )
            row_dict = cursor.fetchone()
            while row_dict:
                x_data.append(row_dict['trade_date'].strftime('%Y-%m-%d'))
                y_data.append([
                    float(row_dict['open_price']), float(row_dict['close_price']),
                    float(row_dict['low_price']), float(row_dict['high_price'])
                ])
                row_dict = cursor.fetchone()
    except pymysql.MySQLError as err:
        print(err)
    finally:
        conn.close()
    return {'x': x_data, 'y': y_data}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
