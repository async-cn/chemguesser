from flask import render_template, abort
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

@main.route('/docs/<path:doc_path>')
def docs(doc_path):
    """文档页面
    
    访问URL: /docs/.../<docname>
    - ... 为文档相对路径（不含.字符）
    - <docname> 为文档名
    
    例如：
    - /docs/group → 查找 docs/group.md
    - /docs/about/group → 查找 docs/about/group.md
    """
    # 解析路径
    path_parts = doc_path.split('/')
    doc_name = path_parts[-1] if path_parts[-1] else path_parts[-2] if len(path_parts) > 1 else ''
    relative_path = '/'.join(path_parts[:-1]) if len(path_parts) > 1 else ''
    
    # 安全验证：检查路径中不含.字符
    if '.' in doc_path:
        # 404
        doc_path = 'doc404'
        relative_path = ''
    
    # 构造文件路径
    base_dir = os.getcwd()
    if relative_path:
        file_path = os.path.join(base_dir, 'docs', relative_path, f'{doc_name}.md')
    else:
        file_path = os.path.join(base_dir, 'docs', f'{doc_name}.md')
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        # 尝试使用doc404.md
        file_path = os.path.join(base_dir, 'docs', 'doc404.md')
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        # 读取失败时使用默认404内容
        content = '# 文档不存在\n\n抱歉，您请求的文档不存在。'
    
    # 将markdown转换为HTML
    doc_html = markdown.markdown(content)
    
    return render_template('docs.html', doc_html=doc_html, doc_title=doc_name)

@main.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@main.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403