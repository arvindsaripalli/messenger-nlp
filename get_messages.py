import argparse
import getpass
import joblib
import os
from fbchat import Client
from fbchat.models import *
from datetime import datetime

class MessageDownloader:
    def __init__(self, args):
        """
            Authenticates the Message downloader.
            args: Command line arguments.
        """
        self.names = args.names
        self.thread_ids = args.ids
        self.client = self.authenticate()

    def authenticate(self):
        """
            Returns an fbchat.Client object after signing into Messenger.
        """
        user = str(input("Username: "))
        password = getpass.getpass()
        client = Client(user, password)
        return client
    
    def get_valid_queries(self):
        """
            Returns a list of tuples of valid threads. 
            Each tuple is of the form (thread id, thread name)
        """
        valid_threads = []
        
        # Validate thread ids if thread ids are given.
        if self.thread_ids:
            for tid in self.thread_ids:
                # Add thread name and its id if it is valid.
                try:
                    thread = self.client.fetchThreadInfo(tid)[tid]
                    valid_threads.append((thread.uid, thread.name))
            
                # Ignore invalid ids.    
                except FBchatException as e: 
                    pass

        # Validate names if names are given.
        if self.names:
            for name in self.names:
                # Add thread name and its id if it is valid.
                try:
                    thread = self.client.searchForThreads(name)[0]
                    valid_threads.append((thread.uid, thread.name))
                
                # Ignore invalid thread.    
                except FBchatException as e: 
                    pass
            
        if not len(valid_threads):
            print("Error: No valid threads were found with the given queries")
            exit(1)

        return valid_threads     

    def download_messages(self):
        query_threads = self.get_valid_queries()
        print(query_threads)

def process_message(message, user_id):
    if message.author == user_id or message == "None":
        return None
    return message


def main():
    search_name, limit = get_args()
    client = login()
    user_id = client.uid
    thread = client.searchForThreads(search_name)[0]

    # Gets the last 'limit' number of messages sent to the conversation.
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
    # Command line argument parsing.
    parser = argparse.ArgumentParser(description='Downloads Facebook Messenger Convserations.')
    parser.add_argument('--names', nargs='+', help='Names of user conversation to search for and get messages from.')
    parser.add_argument('--ids', nargs='+', help='Messenger conversation ids to get messages from.')
    parser.add_argument('--limit', default=30, help='Number of messages to be recorded')

    args = parser.parse_args()

    # Throw an error if no names or thread ids were supplied.
    if not args.names and not args.ids:
        print("Error: At least one of --names or --ids is required.")
        parser.print_help()
        exit(1)

    md = MessageDownloader(args)
    md.download_messages()
