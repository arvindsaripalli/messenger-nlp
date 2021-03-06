import joblib
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

class FormatData:
    def __init__(self):
        self.labels = self.__get_labels()
        self.messages = self.__get_messages()
        self.vocabulary = self.__bag_of_words()
        self.counts = self.__get_counts()
        self.__term_freq_inverse_doc()


    def __get_labels(self):
        labels = []
        for file in os.listdir('./messages/'):
            filename = file.split('.')[0]
            labels.append(filename)
        return labels

    def __get_messages(self):
        """
        Returns list containing a list with all messages from each
        person.
        """
        messages = []

        # Find pickle files to load from.
        for file in os.listdir('./messages/'):
            filename = file.split('.')[0]
            message_objects = joblib.load('./messages/' + file)
            #messages[filename] = self.__get_message_text(message_objects=message_objects)
            messages.append(self.__get_message_text(message_objects=message_objects))

        return messages

    def __get_message_text(self, message_objects):
        """
        Returns list of strings of messages sent by a single user.
        """
        messages = []
        for message in message_objects:
            # Check if message text is valid.
            if message.text is not None and message != '':
                messages.append(message.text)
        return messages

    def __bag_of_words(self):
        """
        Returns a list of every word occurrence in the dataset. Unique to bag of words model,
        but a bigram or trigram vocabulary extraction can be implemented.
        """
        vocabulary = []
        for person in self.messages:
            for message in person:
                for word in message.split(' '):
                    if word not in vocabulary:
                        vocabulary.append(word)
        return vocabulary

    def __get_counts_manually(self):
        """
        Returns a numpy array of lists of count vectors for each message sent by a person.
        Manual implementation of CountVectorizer using dense matrices. CountVectorized, however
        ignores some words in the vocab such as emojis and may be less helpful.
        """
        counts = []
        for i in range(len(self.messages)):
            counts.append([])
            # Get count vector for each message and append to user's message counts.
            for message in self.messages[i]:
                message_count = self.__get_word_count_vector(message)
                counts[i].append(message_count)
        return np.array(counts)

    def __get_word_count_vector(self, message):
        """
        Returns a list of counts whose positions correspond to the words
        in the vocabulary.
        """
        count = [0] * len(self.vocabulary)
        for word in message.split(' '):
            count[self.vocabulary.index(word)] += 1
        return count

    def __get_counts(self):
        """
        Returns a sparse matrix of lists of count vectors for each message sent by a person.
        """
        all_messages = []
        counts = []
        count_vect = CountVectorizer(vocabulary=self.vocabulary)

        for person in self.messages:
            count_vector = count_vect.fit_transform(person)
            counts.append(count_vector)

        return counts

    def __term_freq_inverse_doc(self):
        tfidf_transformer = TfidfTransformer()
        for i in range(len(self.counts)):
            self.counts[i] = tfidf_transformer.fit_transform(self.counts[i])

    def get_dataset(self):
        """
        Shuffle and split data into training and testing.
        """
        X = []
        y = []
        for i in range(len(self.counts)):
            person = self.counts[i]
            for count_vector in person:
                X.append(count_vector.toarray()[0])
                y.append(i)

        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.2,
                                                            random_state=42)

        return X_train, X_test, y_train, y_test, self.labels
