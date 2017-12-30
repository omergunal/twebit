import tweepy
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

#consumer key, consumer secret, access token, access secret.
consumerKey="XXXX"
consumerSecret="XXXX"
accessToken="XXXX-XXXX"
accessSecret="XXXX"

train = []
for i in open('data/pos.txt'): # get train data from pos.txt and neg.txt
        train.append([i.rstrip('\n'), 'pos'])
for j in open('data/neg.txt'):
        train.append([j.rstrip('\n'), 'neg'])

test = []
for z in open('data/test/testPos.txt'): # get test data from testPos.txt and testNeg.txt
    test.append([z.rstrip('\n'), 'pos'])
for x in open('data/test/testNeg.txt'):
    test.append([x.rstrip('\n'), 'neg'])

cl = NaiveBayesClassifier(train)

# Classify some text
print(cl.classify("bitcoin is rising to $20000"))  # "pos"
print(cl.classify("Bitcoin is a big bubble"))   # "neg"

print(cl.accuracy(test))
