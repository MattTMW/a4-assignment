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

    def __repr__(self):
        return f"<MESSAGE FROM {self.sender} TO {self.recipient}>"


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None,
                 profile_directory="C:/Users/User/PycharmProjects/a4-assignment/profiles"):
        self.token = ''
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.profile_directory = profile_directory
        self.profile_path = Path(profile_directory) / f"{username}.dsu"
        self.profile = Profile(dsuserver, username, password)
        self.messages = []

        try:
            self.join_server()
            print("Profile loaded successfully.")
        except DsuFileError:
            print("No profile found.")


    def join_server(self):
        self.profile.load_profile(self.profile_path)
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
            pass
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

            #appends message to user profile
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
        message_lst = []
        try:
            if self.token != '':
                new_message = ds_protocol.retrieve_new_message(self.token, message_type)
                print("New_message:", new_message)
                server_response = self.send_to_server(new_message)
                print("server response", server_response)
                for msg in server_response['response']['messages']:
                    recipient = msg.get('recipient', '')
                    sender = msg.get('from', '')
                    message = msg.get('message', '')
                    timestamp = msg.get('timestamp', '')
                    direct_message = DirectMessage(sender, recipient, message, timestamp)
                    message_lst.append(direct_message)
                    # Add the message to the recipient's profile
                    self.profile.add_from(sender, message, timestamp)
                    self.profile.save_profile(self.profile_path)

                # Sort messages by timestamp
                message_lst.sort(key=lambda x: x.timestamp)

                print(message_lst)
                return message_lst

            elif self.token == '':
                more_messages = self.profile.message_from
                for message in more_messages:
                    user_message = ds_protocol.retrieve_offline_message(message)
                    message_lst.append(DirectMessage(sender = '', recipient=user_message.sender, message=user_message.message, timestamp=user_message.timestamp))
                return message_lst
        except OSError:
            print("ERROR connect to internet!")
        except Exception as e:
            print("Error retrieving messages:", e)


    def retrieve_new(self) -> list:
        return self.retrieve_messages('new')

    def retrieve_all(self) -> list:
        return self.retrieve_messages('all')

    def retrieve_contacts(self) -> list:
        return self.profile.recipients
