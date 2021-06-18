import random

import pymysql
from flask import Flask, redirect, request

from utils import get_mysql_connection

app = Flask(__name__)


@app.route('/')
def show_index():
    # 将请求重定向到static目录下的index.html
    return redirect('/static/index.html')


# API - Application Programming Interface - 应用程序编程接口
# 网络API（网络数据接口）- 请求这个URL就可以获得对应的数据（通常是JSON格式）
@app.route('/api/general_data')
def get_general_data():
    conn = get_mysql_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('select sum(orderAmount) from tb_order')
            gmv = round(float(cursor.fetchone()[0]) / 10000, 2)
            cursor.execute('select sum(payment) from tb_order')
            sales = round(float(cursor.fetchone()[0]) / 10000, 2)
            cursor.execute('select sum(payment) from tb_order where chargeback="否"')
            real_sales = round(float(cursor.fetchone()[0]) / 10000, 2)
            cursor.execute('select sum(payment) / count(distinct userID) from tb_order where chargeback="否"')
            arppu = round(float(cursor.fetchone()[0]), 2)
    except pymysql.MySQLError as err:
        print(err)
    finally:
        conn.close()
    return {'results': [
        {'name': 'GMV', 'value': gmv, 'unit': '万元'},
        {'name': '销售额', 'value': sales, 'unit': '万元'},
        {'name': '实际销售额', 'value': real_sales, 'unit': '万元'},
        {'name': '客单价', 'value': arppu, 'unit': '元'}
    ]}


@app.route('/api/sales_data')
def get_sales_data():
    y1_data = [random.randrange(10, 41) for _ in range(6)]
    y2_data = [random.randrange(20, 51) for _ in range(6)]
    return {'y1': y1_data, 'y2': y2_data}


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
    app.run(host='0.0.0.0', debug=True)
