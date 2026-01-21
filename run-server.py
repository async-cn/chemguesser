#!/usr/bin/env python3
"""
ChemGuesser 项目启动脚本
用于一键启动项目，支持不同环境配置
"""

import os
import sys
import logging
from dotenv import load_dotenv
from app import create_app, db

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """检查环境配置"""
    logger.info("检查环境配置...")
    
    # 加载环境变量
    if not load_dotenv():
        logger.error("无法加载 .env 文件，请确保 .env 文件存在且配置正确")
        return False
    
    # 检查必要的环境变量
    # required_vars = [
    #     "BASEURL", "APIKEY", "MODEL", "ROOT_KEY",
    #     "SMTP_SERVER", "SMTP_PORT", "SMTP_ADDR", "SMTP_KEY",
    #     "MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DB"
    # ]
    
    # missing_vars = []
    # for var in required_vars:
    #     if not os.getenv(var):
    #         missing_vars.append(var)
    
    # if missing_vars:
    #     logger.error(f"缺少必要的环境变量: {', '.join(missing_vars)}")
    #     return False
    
    # 检查 API Key 是否为默认值
    if os.getenv("APIKEY") == "your_api_key":
        logger.error("API Key 仍为默认值，请在 .env 文件中设置正确的 API Key")
        return False
    
    logger.info("环境配置检查通过")
    return True

def initialize_database(app, db):
    """初始化数据库"""
    logger.info("初始化数据库...")
    try:
        with app.app_context():
            # 创建所有表
            db.create_all()
            logger.info("数据库初始化完成")
            return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False

def start_server():
    """启动服务器"""
    logger.info("启动 ChemGuesser 服务器...")

    # 检查环境
    if not check_environment():
        import sys
        sys.exit(1)

    try:
        import sys
        sys.path.append('.')
        app = create_app()

        # 初始化数据库
        if not initialize_database(app, db):
            sys.exit(1)

        # 加载.env
        host = os.getenv("WEBSITE_ADDR", "localhost")
        port = int(os.getenv("WEBSITE_PORT", "5000"))
        debug = os.getenv("FLASK_ENV") == "development"

        logger.info(f"服务器将在 http://{host}:{port} 启动")
        logger.info(f"运行环境: {'开发模式' if debug else '生产模式'}")
        logger.info("按 Ctrl+C 停止服务器")

        app.run(host=host, port=port, debug=debug)

    except ImportError as e:
        logger.error(f"导入模块失败: {e}")
        logger.error("请确保已安装所有依赖 (pip install -r requirements.txt)")
        sys.exit(1)
    except Exception as e:
        logger.error(f"启动服务器失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()