import random

from flask import Flask

app = Flask(__name__)


@app.route('/')
def say_hello():
    fruits_list = [
        '苹果', '香蕉', '山竹', '榴莲', '杨梅', '草莓', '蓝莓', '石榴', '番茄',
        '杨桃', '哈密瓜', '西瓜', '葡萄', '百香果', '樱桃', '车厘子', '荔枝'
    ]
    fruits_count = random.randrange(3, 6)
    selected_fruits = random.sample(fruits_list, fruits_count)
    page_code = '<h1 style="text-align: center">今日推荐的水果</h1>'
    page_code += '<hr>'
    page_code += '<ul>'
    for fruit in selected_fruits:
        page_code += f'<li>{fruit}</li>'
    page_code += '</ul>'
    return page_code


if __name__ == '__main__':
    app.run(host='10.7.174.103', debug=True)
