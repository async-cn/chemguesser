from flask import render_template
from app.main import main

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/rules')
def rules():
    return render_template('rules.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@main.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403