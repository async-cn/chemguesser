from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User
from app.users import users

# 创建admin蓝图
admin = Blueprint('admin', __name__, url_prefix='/admin')

# 访问控制装饰器，仅允许root用户访问
def root_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('users.login'))
        if current_user.username != 'root':
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/accounts-manager')
@login_required
@root_required
def accounts_manager():
    """账户管理页面"""
    return render_template('admin/accounts_manager.html', title='账户管理')

@admin.route('/accounts')
@login_required
@root_required
def get_accounts():
    """获取账户列表
    
    请求参数：
        page: 页码，默认为1
        per_page: 每页数量，默认为30
    
    返回：
        JSON格式的账户列表，包含分页信息
    """
    try:
        # 获取请求参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))
        
        # 验证参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 30
        
        # 查询账户列表
        pagination = User.query.order_by(User.id).paginate(page=page, per_page=per_page, error_out=False)
        users_list = [{"id": user.id, "username": user.username, "email": user.email, "elo_score": user.elo_score, "created_at": user.created_at.isoformat()} for user in pagination.items]
        
        # 构建响应数据
        response = {
            "status": "success",
            "data": {
                "users": users_list,
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                    "next_num": pagination.next_num,
                    "prev_num": pagination.prev_num
                }
            },
            "message": "账户列表获取成功"
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"获取账户列表失败: {str(e)}"
        }), 500

@admin.route('/accounts/<int:user_id>', methods=['DELETE'])
@login_required
@root_required
def delete_account(user_id):
    """删除账户
    
    请求参数：
        user_id: 要删除的用户ID
    
    返回：
        JSON格式的响应
    """
    try:
        # 查找用户
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "status": "error",
                "message": "用户不存在"
            }), 404
        
        # 不允许删除root用户
        if user.username == 'root':
            return jsonify({
                "status": "error",
                "message": "不允许删除root用户"
            }), 403
        
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "账户删除成功"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"删除账户失败: {str(e)}"
        }), 500
