import json
import ds_protocol


#For testing just use assert
token = "321"
username = "mark"
password = "nah"
message_type = 'all'

json_msg = json.dumps({"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}})
print(ds_protocol.extract_json(json_msg))
response = '{"response": {"type": "ok", "message": "Direct message sent"}}'
print(ds_protocol.server_response(response))
print(ds_protocol.retrieve_all_message(token, message_type))

