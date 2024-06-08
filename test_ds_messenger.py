import unittest
from unittest.mock import MagicMock
from ds_messenger import DirectMessenger, DirectMessage


# Mock Profile class to avoid file I/O and actual server connections
class MockProfile:
    def __init__(self, dsuserver, username, password):
        self.dsuserver =
        self.username = username
        self.password = password
        self.token = ''
        self.messages = []
        self.recipients = []

    def load_profile(self, path):
        pass

    def save_profile(self, path):
        pass

    def add_message(self, message):
        self.messages.append(message)

    def add_recipient(self, recipient):
        self.recipients.append(recipient)

    def add_from(self, sender, message, timestamp):
        self.messages.append({"from": sender, "message": message, "timestamp": timestamp})


class TestDirectMessenger(unittest.TestCase):
    def setUp(self):
        self.dsuserver = 'testserver.com'
        self.username = 'testuser'
        self.password = 'testpass'

        # Replace the profile with a mock profile
        DirectMessenger.profile = MockProfile(self.dsuserver, self.username, self.password)
        self.messenger = DirectMessenger(self.dsuserver, self.username, self.password)

    def test_join_server_success(self):
        # Simulate a successful server join
        self.messenger.profile.token = '12345'
        self.assertTrue(self.messenger.join_server())
        self.assertEqual(self.messenger.token, '12345')

    def test_send_message_success(self):
        # Simulate a successful message send
        self.messenger.token = '12345'
        self.messenger.send_to_server = MagicMock(return_value={"response": {"type": "ok"}})

        result = self.messenger.send_message('Hello', 'recipient_user')
        self.assertTrue(result)

    def test_send_message_failure(self):
        # Simulate a failed message send
        self.messenger.token = '12345'
        self.messenger.send_to_server = MagicMock(return_value={"response": {"type": "error"}})

        result = self.messenger.send_message('Hello', 'recipient_user')
        self.assertFalse(result)

    def test_retrieve_messages(self):
        # Simulate retrieving messages
        self.messenger.token = '12345'
        self.messenger.send_to_server = MagicMock(return_value={
            "response": {
                "messages": [
                    {"recipient": "testuser", "from": "sender1", "message": "Hello", "timestamp": "1622505600"},
                    {"recipient": "testuser", "from": "sender2", "message": "Hi", "timestamp": "1622505700"}
                ]
            }
        })

        messages = self.messenger.retrieve_messages('new')
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].sender, 'sender1')
        self.assertEqual(messages[0].message, 'Hello')
        self.assertEqual(messages[1].sender, 'sender2')
        self.assertEqual(messages[1].message, 'Hi')


if __name__ == '__main__':
    unittest.main()