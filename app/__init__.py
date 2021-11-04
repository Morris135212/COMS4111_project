# -*- coding: utf-8 -*-
from flask import Flask  # 引入 flask
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)  # 实例化一个flask 对象
# from app import views

from app import config
from app.views import competitions, dataset, courses
