import unittest

import json
from app.test.base import BaseTestCase

from app.main.service.user_service import create_new_user, save_changes

email = 'admin@dorokhin.moscow'
username = 'admin'
password = 'changeme'
wrong_password = 'wrong_password'

valid_user_data = dict(
            email=email,
            password=password
        )


def create_user_with_admin_privileges():
    user = {'email': 'admin@dorokhin.moscow',
            'username': 'admin',
            'password': 'changeme'
            }
    save_changes(create_new_user(user, True))


def login_user(self, user_data):
    return self.client.post(
        '/auth/login',
        data=json.dumps(user_data),
        content_type='application/json'
    )


class TestAdminPrivileges(BaseTestCase):
    def test_admin_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # admin user creation
            create_user_with_admin_privileges()

            # admin user login
            response = login_user(self, valid_user_data)
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
            resp_login = login_user(self, valid_user_data)
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

    def test_get_user_by_id(self):
        with self.client:
            """
            Test get user by public_id
            """
            # user registration
            create_user_with_admin_privileges()
            # user login
            resp_login = login_user(self, valid_user_data)
            data_login = json.loads(resp_login.data.decode())

            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            logget_user = self.client.get(
                '/user/',
                headers=dict(
                    Authorization='' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )

            get_user_bypublic_id = self.client.get(
                '/user/{0}'.format(json.loads(logget_user.data.decode())['data'][0]['public_id']),
                headers=dict(
                    Authorization='' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )

            self.assertEqual(200, get_user_bypublic_id.status_code)
            self.assertEqual('admin', json.loads(get_user_bypublic_id.data.decode())['username'])
            self.assertEqual('admin@dorokhin.moscow', json.loads(get_user_bypublic_id.data.decode())['email'])
            self.assertEqual(None, json.loads(get_user_bypublic_id.data.decode())['password'])
            self.assertTrue(json.loads(get_user_bypublic_id.data.decode())['public_id'])


if __name__ == '__main__':
    unittest.main()
