import random

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
