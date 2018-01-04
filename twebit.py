
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

nltk.download('stopwords')
nltk.download('punkt')

consumerKey="XXXX"
consumerSecret="XXXX"
accessToken="XXXX-XXXX"
accessSecret="XXXX"

stop_words = set(stopwords.words('english'))

class listener(StreamListener):
    x = 0
    y = 0
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        tweet = re.sub(r"http\S+", "", tweet)
        analysis = TextBlob(tweet)
        try:
            if analysis.detect_language() == 'en':
                print(tweet,cl.classify(tweet))
                try:
                    if cl.classify(tweet) == 'pos':
                        listener.y += 1
                    else:
                        listener.y -= 1
                    plt.ion()
                    listener.x += 1
                    plt.scatter(listener.x,listener.y)
                    plt.pause(0.05)
                except:
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
            filtered_sentence = [w for w in word_tokens if not w in stop_words] # filter stop words
            arr.append([filtered_sentence, group])

def main():
    auth = OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    train = []
    test = []
    getData('data/pos.txt', 'pos',train) #get data from txt file
    getData('data/neg.txt', 'neg',train)
    getData('data/test/testPos.txt', 'pos', test)
    getData('data/test/testNeg.txt', 'neg', test)

    global cl
    cl = NaiveBayesClassifier(train)

    while True: # get tweets from twitter
        print(cl.accuracy(test))
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["bitcoin"], async = True)
        time.sleep(60)
        twitterStream.disconnect()


if __name__ == "__main__":
    main()
