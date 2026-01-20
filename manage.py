from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# 初始化迁移工具
migrate = Migrate(app, db)
manager = Manager(app)

# 添加迁移命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()