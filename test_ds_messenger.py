import unittest
import ds_messenger


class TestDirectMessenger(unittest.TestCase):

    def information(self):
        self.dsuserver = '168.235.86.101'
        self.username = 'chairbro'
        self.password = 'bro'
        self.messenger = ds_messenger.DirectMessenger(self.dsuserver, self.username, self.password)

    def test_join_server(self):
        result = self.messenger.join_server()
        self.assertTrue(result, "Failed to join server")  #server should fail

    def test_send_message_valid(self):
        self.messenger.join_server()  #join server
        result = self.messenger.send_message("Hello, world!", "ethanboy")  # valid message
        self.assertTrue(result, "Failed to send valid message")

    def test_retrieve_all_messages(self):
        self.messenger.join_server()  #join server
        self.messenger.send_message("will it work?", "ethanboy")  #sends message
        all_messages = self.messenger.retrieve_all()
        self.assertIsInstance(all_messages, list, "Failed to retrieve all messages")
        self.assertGreater(len(all_messages), 0, "No messages retrieved")

    def test_invalid_server(self):
        self.messenger.dsuserver = 'invalid.server.address'  #string for server
        result = self.messenger.join_server()
        self.assertFalse(result, "Should not be able to join invalid server")

if __name__ == '__main__':
    unittest.main()