# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Matthew Truong
# mntruon04@uci.edu
# 24588592

from pathlib import Path
import shlex
from Profile import Profile, DsuFileError, DsuProfileError, Post
import ds_messenger

port = 3021


def empty_whitespace(text):
    return not text or text.strip == ''


def get_user_choice():
    while True:
        user_choice = input("Provide your command: ")
        if user_choice == "Q":
            return user_choice
        elif user_choice == "C":
            return user_choice
        elif user_choice == "O":
            return user_choice
        elif user_choice == "D":
            return user_choice
        elif user_choice == "R":
            return user_choice
        elif user_choice == "E":  #maybe connect to edit menu?
            return user_choice
        elif user_choice == "P":
            return user_choice
        else:
            print("Please give valid input (C/O/D/R/Q)\n"
                  "Or (E/P) once file is loaded.")


def edit_post(directory_path):
    while True:
        inner_choice = input("Would you like to edit (E) or print (P) the file? (E/P/Q): ")
        if inner_choice.strip() == 'Q':
            break
        elif inner_choice.strip() == 'E':
            edit_menu()
            command = shlex.split(input("Enter your edit command (e.g., [E] [-usr] [username])"))
            edit(directory_path, command)
        elif inner_choice.strip() == 'P':
            print_menu()
            command = shlex.split(input("Enter your print command (e.g., [P] [-pwd])"))
            print_file(directory_path, command)
        else:
            print("Provide a valid input!")


def edit_menu():
    print("You've accessed the edit menu!")
    print("Here are the possible commands.")
    print("E -usr [USERNAME] will edit your username.")
    print("E -pwd [PASSWORD] will edit your password.")
    print("E -bio [BIO] will edit your bio.")
    print("E -addpost [NEWPOST] will make a new post.")
    print("E -delpost [ID] will delete your post at a given index.")


def print_menu():
    print("You've accessed the print menu!")
    print("Here are the possible commands.")
    print("P -usr prints your profile's username.")
    print("P -pwd prints your profile's password.")
    print("P -bio will print your profile's bio.")
    print("P -posts will print your posts.")
    print("P -post [ID] will print your post at that index.")
    print("P -all will all the content in your file.")


def create(user_command):  #gets user_input from main
    file_path = Path(user_command[1])
    if user_command[2] == '-n':  #if user picks -n option, we name the file
        try:
            file_name = user_command[3]  #takes user file name
            directory_path = Path(file_path / (file_name + '.dsu'))  # makes file directory and dsu
            directory_path.touch()
            print("Your file has been created:", directory_path)
            if directory_path.exists():  # checks if file exists
                print("Please create your profile!")
                server = input('Enter the IP address you are uploading your profile to: ')
                user = input('Enter your username: ')  #takes in user_input after creating file
                password = input('Enter your password: ')
                bio = input('Enter bio: ')
                user_profile = Profile(dsuserver=server, username=user, password=password)  #creates user_profile
                if empty_whitespace(bio):
                    print("Cannot enter empty bio!")
                    return None
                user_profile.bio = bio  #also gets user bio
                user_profile.save_profile(str(directory_path))  #saves profile info into file
                print("Your profile has been created!")
            else:
                print("File doesn't exist!")
        except DsuFileError:
            print("DsuFileError, possible directory error.")
        except DsuProfileError:
            print("DsuProfileError, issue loading profile.")
        except FileNotFoundError:
            print("File can't be found.")
        except FileExistsError:
            print("File already exists!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print('Provide an option.')
        return None
    return directory_path


def delete(user_command):  #deletes the dsu file
    delete_directory = Path(user_command[1])  # directory set to this
    if str(delete_directory).endswith('.dsu'):  #checks for .dsu
        try:
            delete_directory.unlink()  #deletes it
            print(f'{delete_directory} DELETED')
        except DsuFileError:
            print("DsuFileError, possible directory error.")
        except FileNotFoundError:
            print("File can't be found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print('ERROR, provide a dsu file.')


def read(user_command):  #reads the dsu file
    file_read = Path(user_command[1])
    if str(file_read).endswith('.dsu'):
        try:
            if file_read.stat().st_size == 0:
                print('EMPTY')
            else:
                print("Here is the content in your file!")
                with open(file_read, 'r') as f:
                    print(f.read())
        except DsuFileError:
            print("DsuFileError, possible directory error.")
        except FileNotFoundError:
            print("File can't be found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print('ERROR, provide a dsu file.')


def open_file(user_command):  #opens file from user
    file_directory = Path(user_command[1])
    if str(file_directory).endswith('.dsu'):  #checks if its dsu
        try:
            user_profile = Profile()
            user_profile.load_profile(str(file_directory))
            print(f'{file_directory} is now open!')  #opens directory
            print(f"IP Server:", user_profile.dsuserver)
            print("Username:", user_profile.username)
            print("Password:", user_profile.password)
            print("Bio:", user_profile.bio)
        except DsuFileError:
            print("DsuFileError, possible directory error.")
        except DsuProfileError:
            print("DsuProfileError, issue loading profile.")
        except FileNotFoundError:
            print("File can't be found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("File isn't a dsu!")
        return None
    return file_directory  #will return file_directory to main


def edit(directory, command_line):  #edits the file
    try:
        user_profile = Profile()
        user_profile.load_profile(str(directory))
        for i in range(1, len(command_line), 2):
            if command_line[i] == '-usr':
                user_profile.username = command_line[i + 1]
                print("Your username has been updated!")  #edits username
            elif command_line[i] == '-pwd':
                user_profile.password = command_line[i + 1]
                print("Your password has been updated!")  #edits password
            elif command_line[i] == '-bio':
                user_profile.bio = command_line[i + 1]
                if empty_whitespace(user_profile.bio):
                    print("Can't have empty bio!")
                else:
                    print("Your bio has been updated!")
                    send_bio = input("Do you want to update your bio on the server? (y/n)") #edits bio
                    if send_bio == 'y':
                        ds_client.send(user_profile.dsuserver, port, user_profile.username, user_profile.password, None,
                                       user_profile.bio)
                        print("Bio updated on the server.")
            elif command_line[i] == '-addpost':
                post_content = (command_line[i + 1])  #adds a post
                if empty_whitespace(post_content):
                    print("Can't have empty post!")
                else:
                    new_post = Post(post_content)
                    user_profile.add_post(new_post)
                    print(new_post)
                    print("You have a new post!")
                    online_post = input("Do you want to post this to the server? (y/n)")
                    if online_post == 'y':
                        server_address = user_profile.dsuserver
                        ds_client.send(server_address, port, user_profile.username, user_profile.password, new_post.get_entry(),
                                       user_profile.bio)
                    elif online_post == 'n':
                        break
                    else:
                        print('Input valid command!')
            elif command_line[i] == '-delpost':  #deletes post w index
                try:
                    post_index = int(command_line[i + 1])  #gets index
                    if 0 <= post_index - 1 < len(user_profile.get_posts()):  #checks if post is in range
                        user_profile.del_post(post_index - 1)
                        print("Your post has been deleted!")
                    else:
                        print('Enter an integer in valid range!')
                except IndexError:
                    print("Enter valid index!")
                except ValueError:
                    print("Please enter an index.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            user_profile.save_profile(str(directory))
    except FileNotFoundError:
        print(f"Profile file not found at: {directory}")
    except DsuFileError as e:
        print(f"Error loading profile: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def print_file(directory, command_line):  #will print stuff from file
    try:
        user_profile = Profile()
        user_profile.load_profile(str(directory))
        for i in range(len(command_line)):  #searches through usr input
            if command_line[i] == '-usr':
                print('Your username is:', user_profile.username)  #prints usr
            elif command_line[i] == '-pwd':
                print('Your password is:', user_profile.password)  #prints password
            elif command_line[i] == '-bio':
                print('Your bio is:', user_profile.bio)  #prints bio
            elif command_line[i] == '-posts':
                posts = user_profile.get_posts()
                for number, user_post in enumerate(posts):
                    print(f"{number}. {user_post.get_entry()}")
                online_post = input("Do you want to post any of these to the server? (y/n)")
                if online_post == 'y':
                    try:
                        index = int(input("Okay! Select the post's index: "))
                        if 0 <= index < len(posts):
                            selected_post = posts[index].get_entry()
                            server_address = user_profile.dsuserver
                            ds_client.send(server_address, port, user_profile.username, user_profile.password,
                                           selected_post, user_profile.bio)
                    except ValueError:
                        print("Input valid value!")
                elif online_post == 'n':
                    break
                else:
                    print('Please provide valid command!')
            elif command_line[i] == '-post':  #prints post w index
                try:
                    post_index = int(command_line[i + 1])
                    if 0 <= post_index < len(user_profile.get_posts()):  #checks if in range
                        posts = user_profile.get_posts()
                        print(f"{post_index}: {posts[post_index].get_entry()}")  #gets index of post
                        online_post = input("Do you want to post any of these to the server? (y/n)")
                        if online_post == 'y':
                            selected_post = posts[post_index].get_entry()
                            server_address = user_profile.dsuserver
                            ds_client.send(server_address, port, user_profile.username, user_profile.password,
                                           selected_post, user_profile.bio)
                        elif online_post == 'n':
                            break
                        else:
                            print('Please provide valid command!')
                    else:
                        print('Enter valid index!')
                except IndexError:
                    print("Enter valid index!")
                except ValueError:
                    print("Please enter an index.")
            elif command_line[i] == '-all':  #prints everything
                print("Username:", user_profile.username)
                print("Password:", user_profile.password)
                print("Bio:", user_profile.bio)
                print("Posts:", user_profile.get_posts())
            user_profile.save_profile(str(directory))
    except FileNotFoundError:
        print(f"Profile file not found at: {directory}")
    except DsuFileError as e:
        print(f"Error loading profile: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    while True:
        user_choice = get_user_choice()
        if user_choice == 'Q':
            quit()
        elif user_choice == 'C':
            try:
                path = input("Okay, and where would you like to make your directory? Input directory: ")
                name_of_file = input("What would you like to name your file? (Input as [-n] [file_name]):")
                command = f"{user_choice} {path} {name_of_file}"
                directory_path = create(shlex.split(command))
                if directory_path:
                    edit_post(directory_path)
            except DsuFileError:
                print("DsuFileError, possible directory error.")
            except Exception as e:
                print("ERROR", {e})
        elif user_choice == 'O':
            try:
                path = input("Okay, what directory do you want to access? Input directory: ")
                command = f"{user_choice} {path}"
                file_directory = open_file(shlex.split(command))
                if file_directory:
                    edit_post(file_directory)
            except DsuFileError:
                print("DsuFileError, possible directory error.")
            except Exception as e:
                print("ERROR", {e})
        elif user_choice == 'D':
            try:
                path = input("Okay, what is the path to the file you want to read? Input path: ")
                command = f"{user_choice} {path}"
                delete(shlex.split(command))
            except Exception as e:
                print("ERROR:", e)
        elif user_choice == 'R':
            try:
                directory_path = input("Okay, what is the path to the file you want to read? Input path: ")
                command = f"{user_choice} {directory_path}"
                read(shlex.split(command))
            except Exception as e:
                print("ERROR:", {e})


if __name__ == "__main__":
    print("Welcome Journalist.")
    user_input = input(
        "With our program, you're able to create, load, delete, read and edit files for your journaling purposes!\n"
        "Would you like to create, load, delete, or read your file? (C/O/D/R)\n"
        "You can also edit or print the content of your file after loading it by using (E/P)\n"
        "Or quit the program using Q!\n"
        "What do you say, Journalist: ")
    main()
