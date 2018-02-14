import joblib
import os


def get_messages(message_objects):
    messages = []
    for message in message_objects:
        messages.append(message.text)
    return messages


def main():
    data = {}
    # Find pickle files to load from.
    for file in os.listdir('./messages/'):
        if file.split('.')[1] == 'pkl':
            # Get messages texts from file as a list, then label list with
            # pickle file name.
            message_objects = joblib.load('./messages/' + file)
            data[file.split('.')[0]] = get_messages(message_objects=message_objects)
    print(data)


if __name__ == '__main__':
    main()
