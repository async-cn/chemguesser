from flask import render_template
import markdown
import os
from app.main import main

@main.route('/')
def home():
    # 读取notice.md文件
    notice_content = ""
    notice_path = os.path.join(os.getcwd(), 'docs', 'notice.md')
    
    if os.path.exists(notice_path):
        with open(notice_path, 'r', encoding='utf-8') as f:
            notice_content = f.read()
    
    # 将markdown转换为HTML
    notice_html = markdown.markdown(notice_content)
    
    return render_template('home.html', notice_html=notice_html)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/rules')
def rules():
    # 读取rules.md文件
    rules_content = ""
    rules_path = os.path.join(os.getcwd(), 'docs', 'rules.md')

    if os.path.exists(rules_path):
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules_content = f.read()

    # 将markdown转换为HTML
    rules_html = markdown.markdown(rules_content)
    return render_template('rules.html', rules_html=rules_html)

@main.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@main.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403