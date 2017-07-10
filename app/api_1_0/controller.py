# -*- coding: utf-8 -*-
from . import api
from .service import *
from ..models import Diaryitem, Project, User
from .. import db

from flask import request, make_response, jsonify, g
import json


@api.route('/')
def index():
    return 'hello world'


@api.route('/save/record', methods=['POST'])
def save_record():
    record = json.loads(request.form.get('data'))
    auth_token = request.form.get('token')
    if User.verify_auth_token(auth_token) is not None:
        print type(record['project'])
        # 创建一个新的日志记录。并保存进数据库
        item = Diaryitem(project_id=record['project'],
                         price=record['price'],
                         remark=record['remark'],
                         time=record['time'])
        db.session.add(item)
        db.session.commit()
        return cross_origin({'success': True})
    return cross_origin({'success': False})


# 根据选择的月份获取这个月的所有消费收入记录
@api.route('/get/record', methods=['GET'])
def get_record():
    month_chosen = request.args.get('month')
    month_range = get_month_start_end(month_chosen)
    # 查询一个时间段内所有记录，根据时间倒序排列
    all_record = Diaryitem.query.filter(Diaryitem.time.between(month_range['start'], month_range['end'])).order_by(db.desc(Diaryitem.time)).all()
    this_time = ''
    month_detail = []
    for record in all_record:
        # 根据record.project_id获得这个project的类型和名字
        project = Project.query.filter_by(id=record.project_id).first()
        if str(record.time)[:10] != this_time:
            income, outgo = 0, 0
            if project.type == 'in':
                income += record.price
            if project.type == 'out':
                outgo += record.price
            new_detail = {
                "date": str(record.time)[:10],
                "income": income,
                "outgo": outgo,
                "detail": [{
                    "time": str(record.time)[11:],
                    "project": project.name,
                    "remark": record.remark,
                    "price": record.price,
                    "type": project.type
                }]
            }
            month_detail.append(new_detail)
            this_time = str(record.time)[:10]
        else:
            if project.type == 'in':
                new_detail['income'] += record.price
            if project.type == 'out':
                new_detail['outgo'] += record.price
            new_detail['detail'].append({
                "time": str(record.time)[11:],
                "project": project.name,
                "remark": record.remark,
                "price": record.price,
                "type": project.type
            })
    month_income = sum([d['income'] for d in month_detail])
    month_outgo = sum([d['outgo'] for d in month_detail])

    result = {
        "month": month_chosen,
        "income": month_income,
        "outgo": month_outgo,
        "overplus": month_income - month_outgo,
        "detail": month_detail
    }

    return cross_origin(result)


# 获得所有的收入支出类型
@api.route('/get/feetype', methods=['GET'])
def get_feetype():
    all_project = Project.query.filter_by().all()
    projects = [(p.name, p.id) for p in all_project]
    return cross_origin(projects)


# 7-10 login
@api.route('/register', methods=['POST'])
def register():
    user_info = json.loads(request.form.get('data'))
    print type(user_info)
    # check数据格式
    if user_info:
        user = User(name=user_info['name'],
                    password=user_info['password'])
        db.session.add(user)
        db.session.commit()

    return jsonify([2])


@api.route('/login', methods=['POST'])
def login():
    user_info = json.loads(request.form.get('data'))
    print user_info
    user = User.query.filter_by(name=user_info['name']).first()
    print user

    if user is not None and user.verify_password(user_info['password']):
        print 'aaaa'
        g.current_user = user
        auth_token = g.current_user.generate_auth_token(expiration=864000)
        return cross_origin({'token': auth_token, 'success': True})
    return cross_origin({'success': False})


@api.route('/verify/token', methods=['POST'])
def verify_token():
    token = request.form.get('token')
    if User.verify_auth_token(token) is not None:
        return cross_origin({'confirmed': True})
    return cross_origin({'confirmed': False})
