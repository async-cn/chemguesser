from flask import request, jsonify
from app.api import api
from app.models import VerificationCode
from app import db
from src.config import Config
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import re
import random
import traceback

@api.route('/send-email-code', methods=['POST'])
def send_email_code():
    try:
        """发送邮箱验证码接口
        
        请求参数：
            email: 用户邮箱
        
        返回：
            JSON格式的响应，包含状态码和消息
        """
        # 获取请求数据
        data = request.get_json()
        email = data.get('email')
        ip = request.remote_addr

        # 验证请求参数
        if not email:
            return jsonify({'status': 'error', 'message': '邮箱地址不能为空'}), 400

        # 验证邮箱格式
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'status': 'error', 'message': '邮箱格式不正确'}), 400

        # 检查请求频率（基于IP和邮箱）
        # 1分钟内同一IP或邮箱只能发送1次
        one_minute_ago = (datetime.now() - timedelta(minutes=1))
        recent_codes = VerificationCode.query.filter(
            (VerificationCode.email == email) | (VerificationCode.ip == ip),
            VerificationCode.created_at >= one_minute_ago
        ).count()

        if recent_codes > 0:
            return jsonify({'status': 'error', 'message': '请求过于频繁，请1分钟后重试'}), 429

        # 生成6位验证码
        code = ''.join(random.choices('0123456789', k=6))

        # 读取邮件模板
        email_template_path = os.path.join(os.getcwd(), 'config', 'regemail.html')
        try:
            with open(email_template_path, 'r', encoding='utf-8') as f:
                email_content = f.read()
        except FileNotFoundError:
            traceback.print_exc()
            return jsonify({'status': 'error', 'message': '邮件模板文件不存在'}), 500

        # 替换模板中的验证码
        email_content = email_content.replace('[verification-code]', code)

        # 发送邮件
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = Config.SMTP_ADDR
            msg['To'] = email
            msg['Subject'] = 'ChemGuesser 注册验证码'

            # 添加HTML内容
            msg.attach(MIMEText(email_content, 'html', 'utf-8'))

            # 连接SMTP服务器
            server = smtplib.SMTP_SSL(Config.SMTP_SERVER, int(Config.SMTP_PORT))
            # server.starttls() # QQ邮箱smtp不支持starttls
            server.login(Config.SMTP_ADDR, Config.SMTP_KEY)

            # 发送邮件
            server.send_message(msg)
            server.quit()
        except Exception as e:
            traceback.print_exc()
            return jsonify({'status': 'error', 'message': f'邮件发送失败: {str(e)}'}), 500

        # 保存验证码到数据库
        verification_code = VerificationCode(
            email=email,
            code=code,
            ip=ip
        )
        db.session.add(verification_code)
        db.session.commit()

        # 返回成功响应
        return jsonify({'status': 'success', 'message': '验证码已发送，请注意查收', 'by_the_way': '项目开发不易，请勿滥用验证码接口，求求了www'}), 200
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500
