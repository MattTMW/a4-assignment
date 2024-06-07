import json
import socket
import ds_protocol
import time
from pathlib import Path
from Profile import Profile, DsuFileError


class DirectMessage:
    def __init__(self, sender, recipient, message, timestamp):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None, profile_directory = "C:/Users/User/PycharmProjects/a4-assignment/profiles"):
        self.token = ''
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.profile_directory = profile_directory
        self.profile_path = Path(profile_directory) / f"{username}.dsu"
        self.profile = Profile(dsuserver, username, password)

        try:
            self.profile.load_profile(self.profile_path)
            print("Profile loaded successfully.")
        except DsuFileError:
            print("No profile found.")

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

    def retrieve_messages(self, message_type) -> list:
        try:
            new_message = ds_protocol.retrieve_new_message(self.token, message_type)
            server_response = self.send_to_server(new_message)

            messages = []
            for msg in server_response['response']['messages']:
                recipient = msg.get('recipient', '')
                sender = msg.get('from', '')
                message = msg.get('message', '')
                timestamp = msg.get('timestamp', '')
                direct_message = DirectMessage(sender, recipient, message, timestamp)
                messages.append(direct_message)

            return messages

        except Exception as e:
            print("Error retrieving messages:", e)
            return []
    def retrieve_new(self) -> list:
        return self.retrieve_messages('new')

    def retrieve_all(self) -> list:
        return self.retrieve_messages('all')
