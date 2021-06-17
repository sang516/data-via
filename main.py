import random

from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def show_index():
    # 将请求重定向到static目录下的index.html
    return redirect('/static/index.html')


# API - Application Programming Interface - 应用程序编程接口
# 网络API（网络数据接口）- 请求这个URL就可以获得对应的数据（通常是JSON格式）
@app.route('/api/fruits')
def get_fruits():
    fruits_list = [
        '苹果', '香蕉', '山竹', '榴莲', '杨梅', '草莓', '蓝莓', '石榴', '番茄',
        '杨桃', '哈密瓜', '西瓜', '葡萄', '百香果', '樱桃', '车厘子', '荔枝'
    ]
    fruits_count = random.randrange(3, 6)
    selected_fruits = random.sample(fruits_list, fruits_count)
    return {'fruits': selected_fruits}


@app.route('/api/general_data')
def get_general_data():
    return {'items': [
        {'icon': 'a1.png', 'value': 16543, 'name': '省重点实验室数'},
        {'icon': 'a2.png', 'value': 9631, 'name': '全省科研项目数'},
        {'icon': 'a3.png', 'value': 36542, 'name': '全省科研成果数'}
    ]}


if __name__ == '__main__':
    app.run(host='10.7.174.103', debug=True)
