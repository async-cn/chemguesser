from dotenv import load_dotenv
import os

# load_dotenv(dotenv_path="../.env")
load_dotenv()

class Config:
    BASEURL = os.getenv("BASEURL")
    APIKEY = os.getenv("APIKEY")
    MODEL = os.getenv("MODEL")
    ROOT_KEY = os.getenv("ROOT_KEY")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_ADDR = os.getenv("SMTP_ADDR")
    SMTP_KEY = os.getenv("SMTP_KEY")
    BATTLE_MODEL = os.getenv("BATTLE_MODEL")
    BATTLE_CONFIRM_TIME_LIMIT = os.getenv("BATTLE_CONFIRM_TIME_LIMIT")
    BATTLE_DAMAGE_BASE = os.getenv("BATTLE_DAMAGE_BASE")
    BATTLE_DAMAGE_SCALE_INCREASEMENT = os.getenv("BATTLE_DAMAGE_SCALE_INCREASEMENT")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    WEBSITE_ADDR = os.getenv("WEBSITE_ADDR")
    WEBSITE_PORT = os.getenv("WEBSITE_PORT")
    
    # Flask SQLAlchemy configuration - 使用SQLite进行开发
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chemguesser.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask session configuration
    SECRET_KEY = os.urandom(24)