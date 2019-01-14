import unittest

import json
from app.test.base import BaseTestCase

from app.main.service.user_service import create_new_user, save_changes

admin_email = 'admin@dorokhin.moscow'
admin_username = 'admin'
admin_password = 'changeme'
wrong_password = 'wrong_password'

email = 'test@dorokhin.moscow'
username = 'test'
password = 'changeme'

valid_admin_data = dict(
            email=admin_email,
            password=admin_password
        )

valid_user_data = dict(
            email=email,
            password=password
        )

wrong_public_user_id = 'af06c82b-ce9f-4a72-8c67-275b1e336dda'
wrong_token = '4c11a3f2-8788-4ecb-825f-d97c0c29f5e6'


def create_user_with_admin_privileges():
    user = {'email': admin_email,
            'username': admin_username,
            'password': admin_password
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
            response = login_user(self, valid_admin_data)
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
            resp_login = login_user(self, valid_admin_data)
            data_login = json.loads(resp_login.data.decode())

            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # pass valid token
            response = self.client.get(
                '/user/',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
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
            create_user_with_admin_privileges()
            resp_login = login_user(self, valid_admin_data)
            data_login = json.loads(resp_login.data.decode())

            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            logget_user = self.client.get(
                '/user/',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )

            get_user_by_public_id = self.client.get(
                '/user/{0}'.format(json.loads(logget_user.data.decode())['data'][0]['public_id']),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )

            self.assertEqual(200, get_user_by_public_id.status_code)
            self.assertEqual('admin', json.loads(get_user_by_public_id.data.decode())['username'])
            self.assertEqual('admin@dorokhin.moscow', json.loads(get_user_by_public_id.data.decode())['email'])
            self.assertEqual(None, json.loads(get_user_by_public_id.data.decode())['password'])
            self.assertTrue(json.loads(get_user_by_public_id.data.decode())['public_id'])

    def test_get_user_with_wrong_id(self):
        with self.client:
            """
            Test get user with wrong public_id
            """
            create_user_with_admin_privileges()
            resp_login = login_user(self, valid_admin_data)

            get_user_by_public_id = self.client.get(
                '/user/{0}'.format(wrong_public_user_id),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )
            self.assertEqual(404, get_user_by_public_id.status_code)

    def test_get_user_with_invalid_token(self):
        with self.client:
            get_user_by_public_id = self.client.get(
                '/user/{0}'.format(wrong_public_user_id),
                headers=dict(
                    Authorization='Bearer {0}'.format(wrong_token)
                )
            )
            self.assertEqual('Invalid token. Please log in again.',
                             json.loads(get_user_by_public_id.data.decode())['message'])
            self.assertEqual('fail', json.loads(get_user_by_public_id.data.decode())['status'])
            self.assertEqual(401, get_user_by_public_id.status_code)

    def test_get_user_with_invalid_token_without_bearer_word(self):
        with self.client:
            get_user_by_public_id = self.client.get(
                '/user/{0}'.format(wrong_public_user_id),
                headers=dict(
                    Authorization='{0}'.format(wrong_token)
                )
            )
            self.assertEqual('Bearer does not exist',
                             json.loads(get_user_by_public_id.data.decode())['message'])
            self.assertEqual('fail', json.loads(get_user_by_public_id.data.decode())['status'])
            self.assertEqual(401, get_user_by_public_id.status_code)

    def test_get_user_without_token(self):
        with self.client:
            get_user_by_public_id = self.client.get(
                '/user/{0}'.format(wrong_public_user_id)
            )
            self.assertEqual('Provide a valid auth token.',
                             json.loads(get_user_by_public_id.data.decode())['message'])
            self.assertEqual('fail', json.loads(get_user_by_public_id.data.decode())['status'])
            self.assertEqual(401, get_user_by_public_id.status_code)

    def test_delete_user_by_id(self):
        with self.client:
            """
            Test delete user by public_id
            """
            create_user_with_admin_privileges()
            user = {'email': email,
                    'username': username,
                    'password': password
                    }
            save_changes(create_new_user(user, False))

            # user login
            resp_login = login_user(self, valid_admin_data)
            data_login = json.loads(resp_login.data.decode())

            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)

            # pass valid token
            response = self.client.get(
                '/user/',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )
            users = json.loads(response.data)['data']

            deleted_user = self.client.delete(
                '/user/{0}'.format(users[1]['public_id']),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )
            self.assertEqual(204, deleted_user.status_code)


if __name__ == '__main__':
    unittest.main()
