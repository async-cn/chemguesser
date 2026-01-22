# app/api 蓝图初始化文件
from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import routes
