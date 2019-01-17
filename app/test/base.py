from flask_testing import TestCase
from flask import current_app
from app.main import db
from manage import app
from app import socketio


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        self.test_client = socketio.test_client(app)
        return app

    def setUp(self):
        with self.app.app_context():
            self.test_app = current_app.test_client()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
