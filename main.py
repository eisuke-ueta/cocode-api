from app import app
from app.commons.config import Config
from app.database import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(debug=Config.APP_DEBUG, host=Config.APP_HOST, port=Config.APP_PORT)


if __name__ == '__main__':
    manager.run()
