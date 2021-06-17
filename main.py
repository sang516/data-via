import random

import pymysql
from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def show_index():
    # 将请求重定向到static目录下的index.html
    return redirect('/static/index.html')


# API - Application Programming Interface - 应用程序编程接口
# 网络API（网络数据接口）- 请求这个URL就可以获得对应的数据（通常是JSON格式）
@app.route('/api/general_data')
def get_general_data():
    return {'items': [
        {'icon': 'house.png', 'value': 16543, 'name': '省重点实验室数'},
        {'icon': 'computer.png', 'value': 9631, 'name': '全省科研项目数'},
        {'icon': 'medal.png', 'value': 36542, 'name': '全省科研成果数'},
        {'icon': 'professor.png', 'value': 13642, 'name': '科研专家数'},
        {'icon': 'equipment.png', 'value': 15536, 'name': '科研仪器经费'},
    ]}


@app.route('/api/sales_data')
def get_sales_data():
    y1_data = [random.randrange(10, 41) for _ in range(6)]
    y2_data = [random.randrange(20, 51) for _ in range(6)]
    return {'y1': y1_data, 'y2': y2_data}


@app.route('/api/stock_data')
def get_stock_data():
    conn = pymysql.connect(host='localhost', port=3306,
                           user='guest', password='Guest.618',
                           database='stock', charset='utf8mb4')
    x_data, y_data = [], []
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                'select trade_date, open_price, close_price, low_price, high_price '
                'from tb_baba_stock where trade_date between "2020-1-1" and "2020-1-31"'
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
