from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    verification_method = SelectField('Verification Method', 
                                      choices=[('email', 'Email Verification'), ('root', 'Root Key Verification')],
                                      validators=[DataRequired()])
    email_code = StringField('Email Code')
    root_key = StringField('Root Key')
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        # 检查用户名合法性：不包含空格、斜杠“/”、反斜杠“\”和井号“#”
        if any(char in username.data for char in [' ', '/', '\\', '#']):
            raise ValidationError('Username cannot contain spaces, slashes (/, \\), or #.')
        # 检查用户名是否已存在
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')