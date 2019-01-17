import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.service.user_service import create_new_user, save_changes

from app.remote_controller import main as main_blueprint
from app import socketio

app = create_app(os.getenv('LIGHTWARE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.register_blueprint(main_blueprint)
socketio.init_app(app)

app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def createsuperuser():
    user = {'email': 'andrew@dorokhin.moscow',
            'username': 'deepblack',
            'password': 'changeme'
            }
    save_changes(create_new_user(user, True))


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
