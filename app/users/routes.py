from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.users.forms import RegistrationForm, LoginForm
from app.models import User, VerificationCode
from src.config import Config
from app.users import users
from datetime import datetime

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # 验证成功，检查验证码或rootkey
        is_valid = False
        
        if form.verification_method.data == 'email':
            # 验证email验证码
            email_code = form.email_code.data.strip()
            if not email_code:
                flash('账户创建失败：验证不通过。', 'danger')
                return render_template('register.html', title='Register', form=form)
            
            # 获取最新的未过期验证码
            latest_code = VerificationCode.query.filter(
                VerificationCode.email == form.email.data,
                VerificationCode.expires_at > datetime.now().timestamp()
            ).order_by(VerificationCode.created_at.desc()).first()
            
            if latest_code and latest_code.code == email_code:
                is_valid = True
        
        elif form.verification_method.data == 'root':
            # 验证rootkey
            root_key = form.root_key.data.strip()
            if root_key == Config.ROOT_KEY:
                is_valid = True
        
        if is_valid:
            # 所有验证通过，创建账户
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('账户创建成功！请前往登录。', 'success')
            return redirect(url_for('users.login'))
        else:
            # 验证不通过
            flash('账户创建失败：验证不通过。', 'danger')
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('登录失败，请检查用户名或密码是否正确。', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')