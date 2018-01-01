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

class listener(StreamListener):

    def on_data(self, data):

        all_data = json.loads(data)
        tweet = all_data["text"]
        analysis = TextBlob(tweet)
        if analysis.detect_language() == 'en':
           print(tweet,cl.classify(tweet))
        time.sleep(0.3)
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)

while True:
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["bitcoin"], async = True)
    time.sleep(60)
    twitterStream.disconnect()

'''# Classify some text
print(cl.classify("bitcoin is rising to $20000"))  # "pos"
print(cl.classify("Bitcoin is a big bubble"))   # "neg"

print(cl.accuracy(test))'''
