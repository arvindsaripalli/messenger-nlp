# messenger-nlp
Determining which message came from who. Text classification on my facebook messages.

## Installation
This project requires Python 3.6+.

```
$ pip install requirements.txt
```

## Usage

1. Download messenger messages:

``` bash

python get_messages.py --names 'Name1' 'Name2' 'etc.' --limit="Number of messages to download per conversation"
```

Alternatively, if you know the ids of your messenger conversations:

``` bash
python get_messages.py --ids 'id1' 'id2' 'etc.' --limit="Number of messages to download per converstaion"
```

The messages download to a ./messages directory in the directory that you run
the script by default. You can specify a different path with the --path flag.

2. Run classification:


```
$ python example.py
```
3. Modify example.py to use different classifiers and add run ```get_messages``` to add more classes.

Currently implemented with a bag of words model, TF-IDF, and a few sklearn classifiers. Plans to add n-gram models, stemming, and other classifiers/networks in the future.
