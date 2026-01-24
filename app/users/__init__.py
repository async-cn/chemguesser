from flask import Blueprint

users = Blueprint('users', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

from app.users import routes, admin_routes