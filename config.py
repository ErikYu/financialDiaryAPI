# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/dbname'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'yyz is here'

    @staticmethod
    def init_app(app):
        pass

config = {
    'development': Config
}
