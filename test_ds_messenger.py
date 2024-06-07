import ds_messenger

dsuserver = '168.235.86.101'
username = 'matlol'
password = 'mat'
messenger = ds_messenger.DirectMessenger(dsuserver, username, password)

print(messenger.join_server())
print("Success!")
print(messenger.send_message("will it work 3", "ethanboy"))
new_messages = messenger.retrieve_new()
print("New", new_messages)
all_messages = messenger.retrieve_all()
print("All", all_messages)



