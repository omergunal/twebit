
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
from textblob import TextBlob
import tweepy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re
import numpy as np
import matplotlib.pyplot as plt

nltk.download('punkt')

consumerKey="xxxx"
consumerSecret="xxxx"
accessToken="xxxx-xxxx"
accessSecret="xxxxx"

stopwords = []
for i in open("stopwords.txt"):
    sword = i.rstrip('\n')
    stopwords.append(sword)

global check
check = []

class listener(StreamListener):
    x = 0
    y = 0
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        tweet = re.sub(r"http\S+", "", tweet)
        analysis = TextBlob(tweet)
        stop_words = set(stopwords)
        filtered_words = set(analysis.words.lower()) - stop_words # remove stop words from tweet
        for i in set(filtered_words): # remove @ tags
            if i[:1] == '@':
                set(filtered_words).remove(i)
        try:
            if analysis.detect_language() == 'en': # english tweets
                if analysis not in check:
                    print(tweet,cl.classify(filtered_words))
                    check.append(analysis)
                    if len(check) > 10:
                        del check[:]
                    if cl.classify(tweet) == 'pos':
                        listener.y += 1
                    elif cl.classify(tweet) == 'neut':
                        pass
                    else:
                        listener.y -= 1
                    plt.ion()
                    listener.x += 1
                    plt.scatter(listener.x,listener.y)
                    plt.pause(0.05)
                else:
                    pass
        except:
            pass

        time.sleep(0.3)
        return(True)
    def on_error(self, status):
        print (status)

def getData(filename,group,arr): # add data to array
    for i in open(filename):
            example_sent = i.rstrip('\n') # read txt file
            example_sent = re.sub(r"http\S+", "", example_sent) # remove url
            word_tokens = word_tokenize(example_sent)
            filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stopwords] # filter stop words
            arr.append([filtered_sentence, group])

def main():
    auth = OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    train = []
    test = []
    getData('data/pos.txt', 'pos',train) #get data from txt file
    getData('data/neg.txt', 'neg',train)
    getData('data/neut.txt', 'neut',train)
    getData('data/test/testNeut.txt', 'neut',test)
    getData('data/test/testPos.txt', 'pos', test)
    getData('data/test/testNeg.txt', 'neg', test)

    global cl
    cl = NaiveBayesClassifier(train)

    while True: # get tweets from twitter
        cl.show_informative_features(5)
        print(cl.accuracy(test))
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["bitcoin"], async = True, stall_warnings=True)
        time.sleep(6000) # check
        twitterStream.disconnect()

if __name__ == "__main__":
    main()
