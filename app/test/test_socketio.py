import unittest
from app.test.base import BaseTestCase


class TestSocketIOFunc(BaseTestCase):
    def test_ping_pong(self):
        test_message = 'Success'
        self.test_client.get_received()
        self.test_client.emit('ping', {'msg': test_message})
        received = self.test_client.get_received()
        self.assertEqual('pong', received[0]['name'])
        self.assertEqual(test_message, received[0]['args'][0]['msg'])


if __name__ == '__main__':
    unittest.main()
