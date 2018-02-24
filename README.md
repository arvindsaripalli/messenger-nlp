# messenger-nlp
Determining which message came from who. Text classification on my facebook messages.

## Installation
This project requires Python 3.6+.

```
$ pip install requirements.txt
```

## Usage
1. Download messenger messages for people to classify:
```
$ python get_messages.py --name="Name to search for" --limit="Number of messages to download"
```
2. Run classification:
```
$ python example.py
```
3. Modify example.py to use different classifiers and add run ```get_messages``` to add more classes.

Currently implemented with a bag of words model, TF-IDF, and a few sklearn classifiers. Plans to add n-gram models, stemming, and other classifiers/networks in the future.