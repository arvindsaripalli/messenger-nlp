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
        self.limit = args.limit
        self.messages_path = args.path
        self.client = self.authenticate()

    def authenticate(self):
        """
            Returns an fbchat.Client object after signing into Messenger.
        """
        user = str(input("Username: "))
        password = getpass.getpass()
        client = Client(user, password)
        return client
    
    def get_threads(self):
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

    def get_messages_from_thread(self, thread_uid):
        """
            Returns a list of message objects from the provided thread id.
        """
        messages = self.client.fetchThreadMessages(thread_id=thread_uid,
                                                   limit=self.limit)

        # Since the message come in reversed order, reverse them
        messages.reverse()

        return messages 
        """
        for message in messages:
            if message.author != self.client.uid:
                msg_dict["recipient"].append(message)
            else:
                msg_dict["user"].append(message)

        return msg_dict
        """
   
    def download_messages(self):
        """
           Finds valid threads from queries and saves them to a messages
           directory. 
        """
        threads = self.get_threads()

        # Create the messages dir if it doesn't exist.
        if not os.path.exists(self.messages_path):
            os.makedirs(self.messages_path)
        
        # Save each conversation to the directory.
        for thread in threads:
            uid, name = thread
            messages = self.get_messages_from_thread(uid)
            msg_dict = {"client_id": self.client.uid, "messages": messages}
            
            # Store the messages for this thread in its own file.
            file_name = '{}_{}.pkl'.format(name, uid)
            file_path = os.path.join(self.messages_path, file_name)
            joblib.dump(msg_dict, file_path)
        
        print("Downloaded {} messages from the following conversations: {}".format(self.limit, threads))

def main():
    # Command line argument parsing.
    parser = argparse.ArgumentParser(description='Downloads Facebook Messenger Convserations.')
    parser.add_argument('--names', nargs='+', help='Names of user conversation to search for and get messages from.')
    parser.add_argument('--ids', nargs='+', help='Messenger conversation ids to get messages from.')
    parser.add_argument('--limit', default=30, help='Number of messages to be recorded.')
    parser.add_argument('--path', default='messages', help='Absolute path to store messages to.')
    args = parser.parse_args()

    # Throw an error if no names or thread ids were supplied.
    if not args.names and not args.ids:
        print("Error: At least one of --names or --ids is required.")
        parser.print_help()
        exit(1)

    md = MessageDownloader(args)
    md.download_messages()
    md.client.logout()

if __name__ == '__main__':
    main()
