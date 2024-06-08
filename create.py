import ds_messenger

dsuserver = '168.235.86.101'
username = 'loc'
password = '12'
messenger = ds_messenger.DirectMessenger(dsuserver, username, password)
messenger.profile.save_profile(messenger.profile_path)
print(messenger.join_server())
print("Success!")
print(messenger.send_message("will it work 3", "soccerboy"))
new_messages = messenger.retrieve_new()
print("New", new_messages)
all_messages = messenger.retrieve_all()
print("All", all_messages)