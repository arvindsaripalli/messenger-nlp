import argparse
import getpass
import joblib
import os
from fbchat import Client


def get_args():
    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('--name', required=True, help='Name of user conversation to get messages from')
    parser.add_argument('--limit', default=30, help='Number of messages to be recorded')

    args = parser.parse_args()
    name = args.name
    limit = int(args.limit)

    return name, limit


def login():
    user = str(input("Username: "))
    password = getpass.getpass()
    client = Client(user, password)
    return client


def process_message(message, user_id):
    if message.author == user_id or message == "None":
        return None
    return message


def main():
    search_name, limit = get_args()
    client = login()
    user_id = client.uid
    thread = client.searchForThreads(search_name)[0]

    # Gets the last 'limit' messages sent to the thread.
    print("Getting messages for {}...".format(thread.name))
    messages = client.fetchThreadMessages(thread_id=thread.uid, limit=limit)

    # Since the message come in reversed order, reverse them
    messages.reverse()

    user_messages = []
    # Prints the content of messages not sent by the author
    for message in messages:
        if message.author != user_id:
            user_messages.append(message)

    if not os.path.exists('messages'):
        os.makedirs('messages')
    joblib.dump(user_messages, './messages/{}.pkl'.format(search_name))

    print("Wrote {} messages to ".format(len(user_messages)), "./messages/{}.pkl".format(search_name))
    
    client.logout()


if __name__ == '__main__':
    main()
