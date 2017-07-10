# -*- coding: utf-8 -*-
from flask import make_response, jsonify


# 根据月份获取开始结束时间
def get_month_start_end(month):
    # month: 2017-07
    # return: dict
    if int(month[:4]) % 4 == 0:
        month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return {
        'start': month + '-01 00:00:00',
        'end': month + '-' + str(month_days[int(month[5:7]) - 1]) + ' 23:59:59'
    }


# 跨域封装
def cross_origin(result):
    response = make_response(jsonify(response=result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
