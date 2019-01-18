import unittest

import json
from app.test.base import BaseTestCase

from app.main.service.user_service import create_new_user, save_changes

admin_email = 'admin@dorokhin.moscow'
admin_username = 'admin'
admin_password = 'changeme'

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


class TestChannel(BaseTestCase):
    def test_create_channel_as_admin(self):
        """ Test for create channel as admin """
        with self.client:
            # Create user with admin privileges
            create_user_with_admin_privileges()

            # Login (get admin token)
            response = login_user(self, valid_admin_data)
            data = json.loads(response.data.decode())
            self.auth_token = data['Authorization']

            # Create channel
            channel_data = {
                "dimmer_state": 50,
                "channel_type": True,
                "state": True,
                "name": "Garage"
            }
            created_channel = self.client.post(
                '/channel/',
                headers=dict(
                    Authorization='Bearer ' + self.auth_token
                ),
                data=json.dumps(channel_data),
                content_type='application/json'
            )
            self.assertEqual(201, created_channel.status_code)
            created_channel_data = json.loads(created_channel.data.decode())
            self.assertEqual('Successfully created.', created_channel_data['message'])
            self.assertEqual('success', created_channel_data['status'])

    def test_create_channel_duplicate_with_public_id(self):
        """ Test for create duplicated channel with same id as previous """
        with self.client:
            # Create user with admin privileges
            create_user_with_admin_privileges()

            # Login (get admin token)
            response = login_user(self, valid_admin_data)
            data = json.loads(response.data.decode())
            self.auth_token = data['Authorization']

            # Create channel
            channel_data = {
                "dimmer_state": 50,
                "channel_type": True,
                "state": True,
                "name": "Garage"
            }
            created_channel = self.client.post(
                '/channel/',
                headers=dict(
                    Authorization='Bearer ' + self.auth_token
                ),
                data=json.dumps(channel_data),
                content_type='application/json'
            )
            created_channel_data = json.loads(created_channel.data.decode())
            # create channel with same id
            duplicated_channel_data = {
                "dimmer_state": 50,
                "channel_type": True,
                "state": True,
                "name": "Garage",
                'public_id': created_channel_data['public_id']
            }
            duplicated_channel = self.client.post(
                '/channel/',
                headers=dict(
                    Authorization='Bearer ' + self.auth_token
                ),
                data=json.dumps(duplicated_channel_data),
                content_type='application/json'
            )
            duplicated_channel_data = json.loads(duplicated_channel.data.decode())
            self.assertEqual(409, duplicated_channel.status_code)
            self.assertEqual('Channel already exists', duplicated_channel_data['message'])
            self.assertEqual('fail', duplicated_channel_data['status'])

    def test_update_channel_data(self):
        """ Test for update channel data """
        with self.client:
            # Create user with admin privileges
            create_user_with_admin_privileges()

            # Login (get admin token)
            response = login_user(self, valid_admin_data)
            data = json.loads(response.data.decode())
            self.auth_token = data['Authorization']

            # Create channel
            channel_data = {
                "dimmer_state": 50,
                "channel_type": True,
                "state": True,
                "name": "Garage"
            }
            created_channel = self.client.post(
                '/channel/',
                headers=dict(
                    Authorization='Bearer ' + self.auth_token
                ),
                data=json.dumps(channel_data),
                content_type='application/json'
            )
            created_channel_data = json.loads(created_channel.data.decode())
            # update channel
            updated_channel_data = {
                "dimmer_state": 100,
                "channel_type": False,
                "state": False,
                "name": "updated name",
            }
            updated_channel = self.client.put(
                '/channel/{0}'.format(created_channel_data['public_id']),
                headers=dict(
                    Authorization='Bearer ' + self.auth_token
                ),
                data=json.dumps(updated_channel_data),
                content_type='application/json'
            )
            self.assertEqual(204, updated_channel.status_code)


if __name__ == '__main__':
    unittest.main()
