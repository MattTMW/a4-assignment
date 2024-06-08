import unittest
import json
import ds_protocol


class TestDSProtocol(unittest.TestCase):

    def information(self):
        self.token = "321"
        self.message_type = 'all'
        self.json_msg = json.dumps({"token": "user_token",
                                    "directmessage": {"entry": "Hello World!", "recipient": "ohhimark",
                                                      "timestamp": "1603167689.3928561"}})
        self.response = '{"response": {"type": "ok", "message": "Direct message sent"}}'
        self.invalid_response = '{"response": {"type": "error", "message": "Invalid request"}}'

    def test_extract_json(self):
        result = ds_protocol.extract_json(self.json_msg)
        self.assertIsInstance(result, dict, "extract_json should return a dictionary")
        self.assertIn('token', result, "Token key missing in extracted JSON")  #test for missing key
        self.assertEqual(result['token'], 'user_token', "Token value mismatch")
        self.assertIn('directmessage', result, "Direct message key missing in extracted JSON")

    def test_server_response(self):
        result = ds_protocol.server_response(self.response)
        self.assertIsInstance(result, dict, "server_response should return a dictionary")
        self.assertIn('response', result, "Response key missing in server response")
        self.assertEqual(result['response']['type'], 'ok', "Response type should be 'ok'")  #tests response
        self.assertEqual(result['response']['message'], 'Direct message sent', "Response message mismatch")

        # Testing with an invalid response
        result = ds_protocol.server_response(self.invalid_response)
        self.assertIsInstance(result, dict, "server_response should return a dictionary")
        self.assertIn('response', result, "Response key missing in server response")  #tests errors
        self.assertEqual(result['response']['type'], 'error', "Response type should be 'error'")
        self.assertEqual(result['response']['message'], 'Invalid request', "Response message mismatch")

    def test_retrieve_all_message(self):
        result = ds_protocol.retrieve_all_message(self.token, self.message_type)
        self.assertIsInstance(result, dict, "retrieve_all_message should return a dictionary")
        self.assertIn('token', result, "Token key missing in retrieve all message response")
        self.assertEqual(result['token'], self.token, "Token value mismatch")  #tests retrieval
        self.assertIn('directmessage', result, "Direct message key missing in retrieve all message response")


if __name__ == '__main__':
    unittest.main()
