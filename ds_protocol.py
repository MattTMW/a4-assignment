# Matthew Truong
# mntruon04@uci.edu
# 24588592

import json
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['type', 'message', 'recipient', 'token', 'timestamp'])


def extract_json(json_msg):
    '''
  Call the json.loads function on a json string and convert it to a response.
  '''
    try:
        json_obj = json.loads(json_msg)
        print(json_obj)
        if 'response' in json_obj:
            response = json_obj['response']
            type_response = response.get('type')
            message = response.get('message')
            token = response.get('token', None)
            return DataTuple(type_response, message, None, token, None)
        elif 'directmessage' in json_obj:
            token = json_obj['token']
            message = json_obj['directmessage']['entry']
            recipient = json_obj['directmessage']['recipient']
            timestamp = json_obj['directmessage']['timestamp']
            return DataTuple(None, message, recipient, token, timestamp)
    except json.JSONDecodeError:
        print("JSON can't be decoded!")
    except KeyError:
        print("Key is missing!")


def send_direct_message(token: str, message: str, recipient: str, timestamp: str) -> dict:
    return {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": timestamp}}


def retrieve_new_message(token: str, message_type: str) -> dict:
    return {"token": token, "directmessage": message_type}


def retrieve_all_message(token: str, message_type: str) -> dict:
    return {"token": token, "directmessage": message_type}


def server_response(response: str) -> dict:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("JSON can't be decoded")
