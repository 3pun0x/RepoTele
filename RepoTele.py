import csv
import os
import sys
import time

from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.sync import TelegramClient
from telethon import errors

__author__ = "Asaf Aprozper"
__copyright__ = "Copyright 2019, Reposify"

SLEEP_TIME = 30
API_LIMIT = 200
TELEGRAM_NAMES_FILE = "Telegram_names.txt"
CONFIG_FILE = "config.csv"
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

suspicious_identifiers = ['shell', 'whoisonline', 'cmd', 'screenshot', 'keylogger', 'aureal', 'sysinfo', 'shellcode',
                      'reverseshell', 'whoami', 'backdoor', 'List all online bots', 'TeleSniff', 'snapshot',
                      'دریافت مخاطبین', 'cmd_exec', 'ракушка', 'دریافت مکان', 'ارتباط جنسی', 'крыса', 'проститутки',
                      'наркотики', 'мотыга', 'секс', 'banker', 'valid cc', 'getpic', 'getscr', 'sysinfo',
                      'whoami', '/computer', '/upload', '/kill', '/download', '/shellcode', '/zip', '/ipdetails']

decoded_suspicious_strings = [x.encode('utf-8') for x in suspicious_identifiers]


def write_to_csv(line):
    full_output_path = os.path.join(SCRIPT_DIR, 'output.csv')
    if os.path.exists(full_output_path):
        append_write = "a"
    else:
        append_write = "w"

    with open(full_output_path, mode=append_write) as csv_file:
        fieldnames = ['Username', 'Type', 'Message', 'String', 'PhoneNum']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if append_write == "w":
            writer.writeheader()
        writer.writerow(line)


def send_message(client, phone_number, user_name):
    try:
        # Get entity of the username
        receiver = client.get_entity(user_name)
        type_of_receiver = str(type(receiver))

        # Verify if the username is BOT
        if "User" in type_of_receiver:
            if receiver.bot:
                print("BOT Detected - Sending Commands".format(user_name))
                client.send_message(user_name, '/start')
                print("Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
                client.send_message(user_name, '/help')
                print("Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
                for message in client.iter_messages(user_name, limit=10):
                    message_text = message.text
                    decoded_message = message_text.encode("utf-8")
                    for decoded_suspicious_string in decoded_suspicious_strings:
                        if decoded_suspicious_string in decoded_message:
                            row = {'Username': user_name, 'Type': "BOT", 'Message': message_text,
                                   'String': decoded_suspicious_string,
                                   'PhoneNum': phone_number}
                            write_to_csv(row)
                            print("Found Malicious BOT!")

        # Verify if the username is Channel\Group
        elif "Channel" in type_of_receiver:
            print("Found Channel\\Group - Searching for Malicious Messages")
            for message in client.iter_messages(user_name, limit=10):
                if message.text:
                    message_text = message.text
                    decoded_message = message_text.encode("utf-8")
                    for decoded_suspicious_string in decoded_suspicious_strings:
                        if decoded_suspicious_string in decoded_message:
                            row = {'Username': user_name, 'Type': "Channel\\Group", 'Message': message_text,
                                   'String': decoded_suspicious_string,
                                   'PhoneNum': phone_number}
                            write_to_csv(row)
                            print("Found Malicious Channel\\Group!")

        else:
            print("{} is a regular User, continuing to the next user_name".format(str(user_name)))

    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print("Stooped at bot name: {}", user_name)
        client.disconnect()
        sys.exit()

    except errors.FloodWaitError:
        print("Error: API Limit")
        client.disconnect()
        return "API Limit"

    except Exception as e:
        print(e)


def list_of_telegram_accounts(client, phone):
    try:
        username_counter = 0
        with open(TELEGRAM_NAMES_FILE, 'r') as io_list_telegram_names:
            list_telegram = io_list_telegram_names.readlines()
            new_list = list_telegram[:]

            for telegram_name in list_telegram:
                # Telegram API limit
                if username_counter < API_LIMIT:
                    username_counter += 1

                    # Removing new line character
                    telegram_name_without_line = telegram_name.strip()
                    print("Testing #{} {}".format(username_counter, telegram_name_without_line))

                    result = send_message(client, phone, telegram_name_without_line)

                    # Checking if the result is because of exception of API limit
                    if result == "API Limit":
                        print("Changing to the next API")
                        return
                    else:
                        # Delete the username from the list after usage
                        new_list.remove(telegram_name)

    except Exception as e:
        print(e)

    finally:
        # Writing new list of user_names to scan for the next API key
        with open(TELEGRAM_NAMES_FILE, 'w') as new_list_file:
            new_list_file.writelines(new_list)


def connect_to_telegram():
    try:
        # Open config file with SIM cards and APIs
        with open(CONFIG_FILE, newline='') as csv_file:
            for phone, api_id, api_hash in csv.reader(csv_file, delimiter=','):
                client = TelegramClient(phone, api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    client.send_code_request(phone)
                    client.sign_in(phone, input('Enter the code: '))
                else:
                    print("\nConnected with: {}\n".format(phone))
                    list_of_telegram_accounts(client, phone)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    connect_to_telegram()
