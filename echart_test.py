# /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Allen
@contact: 809721414@qq.com
@time: 2018/4/29 17:04
"""
from pyecharts import Bar, Line
from pyecharts.engine import create_default_environment

bar = Bar("我的第一个图表", "这里是副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])

line = Line("我的第一个图表", "这里是副标题")
line.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])

env = create_default_environment('html')

env.render_chart_to_file(bar, path='bar.html')
env.render_chart_to_file(line, path='line.html')
