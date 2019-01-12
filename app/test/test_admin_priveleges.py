import unittest

from app.main import db
from app.main.model.blacklist import BlacklistToken
import json
from app.test.base import BaseTestCase

from app.main.service.user_service import create_new_user, save_changes


def create_user_with_admin_privileges():
    user = {'email': 'admin@dorokhin.moscow',
            'username': 'admin',
            'password': 'changeme'
            }
    save_changes(create_new_user(user, True))


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='admin@dorokhin.moscow',
            password='changeme'
        )),
        content_type='application/json'
    )


class TestAdminPrivileges(BaseTestCase):
    def test_admin_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # admin user creation
            create_user_with_admin_privileges()

            # admin user login
            response = login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.auth_token = data['Authorization']
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(200, response.status_code)

    def test_get_user_list(self):
        """ Test get user list
            this action require admin token
        """
        with self.client:
            # user registration
            create_user_with_admin_privileges()

            # user login
            resp_login = login_user(self)
            data_login = json.loads(resp_login.data.decode())

            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # pass valid token
            response = self.client.get(
                '/user/',
                headers=dict(
                    Authorization='' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )
            self.assertEqual(200, response.status_code)
            self.assertEqual('admin', json.loads(response.data.decode())['data'][0]['username'])
            self.assertEqual('admin@dorokhin.moscow', json.loads(response.data.decode())['data'][0]['email'])
            self.assertEqual(None, json.loads(response.data.decode())['data'][0]['password'])
            self.assertTrue(json.loads(response.data.decode())['data'][0]['public_id'])

