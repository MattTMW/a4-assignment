import json
import socket
import ds_protocol
import time
from Profile import Profile, DsuFileError


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = ''
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.profile = Profile(dsuserver, username, password)
        self.profile_path = 'test1.dsu'

        # Load existing profile data if available
        try:
            self.profile.load_profile(self.profile_path)
            print("Profile loaded successfully.")
        except DsuFileError:
            print("No existing profile found, starting fresh.")

    def join_server(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
                my_socket.connect((self.dsuserver, 3021))
                print("Connected to server")

                sent_message = my_socket.makefile('w')
                receive = my_socket.makefile('r')

                join_message = json.dumps(
                    {"join": {"username": self.username, "password": self.password, "token": self.token}})
                print("Join message:", join_message)
                sent_message.write(join_message + '\r\n')
                sent_message.flush()

                response = receive.readline()
                print("Server response: ", response)
                response = ds_protocol.extract_json(response)

                if response.type != 'ok':
                    print("Failed to join server.")
                    return False

                self.token = response.token
                print("User token:", self.token)
                return True

        except OSError:
            print("Make sure to be connected to internet!")
            return False
        except Exception as e:
            print('ERROR:', {e})
            return False

    def send_message(self, message: str, recipient: str) -> bool:
        try:
            timestamp = str(time.time())
            directmessage = ds_protocol.send_direct_message(self.token, message, recipient, timestamp)
            response = self.send_to_server(directmessage)
            if response['response']['type'] != 'ok':
                return False

            # Append the message and recipient to the profile
            self.profile.add_message(message)
            self.profile.add_recipient(recipient)
            self.profile.save_profile(self.profile_path)
            print(response)  # TEST
            return True
        except Exception as e:
            print(e)
            return False

    def send_to_server(self, message: dict) -> dict:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
                my_socket.connect((self.dsuserver, 3021))
                sent_message = my_socket.makefile('w')
                receive = my_socket.makefile('r')

                sent_message.write(json.dumps(message) + '\r\n')
                sent_message.flush()

                response = receive.readline()
                return json.loads(response)
        except Exception as e:
            print(e)

    def retrieve_messages(self, message_type):
        try:
            new_message = ds_protocol.retrieve_new_message(self.token, message_type)
            server_response = self.send_to_server(new_message)
            list_responses = list(server_response.items())

            if server_response['response']['type'] != 'ok':
                print("Error in retrieving", message_type, "messages.")
            else:
                return list_responses
        except Exception as e:
            print(e)

    def retrieve_new(self) -> list:
        return self.retrieve_messages('new')

    def retrieve_all(self) -> list:
        return self.retrieve_messages('all')
