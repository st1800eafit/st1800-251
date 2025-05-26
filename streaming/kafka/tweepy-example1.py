#pip3 install tweepy==3.10.0
#python3 tweepy-example1.py 
from __future__ import absolute_import, print_function

import tweepy
import mytwitterKeys

from tweepy import OAuthHandler, Stream, StreamListener

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after

consumer_key = mytwitterKeys.CONSUMER_KEY
consumer_secret = mytwitterKeys.CONSUMER_SECRET
access_token = mytwitterKeys.ACCESS_TOKEN
access_token_secret = mytwitterKeys.ACCESS_TOKEN_SECRET

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

#    def __init__(self,consumer_key, consumer_secret, access_token, access_token_secret):
#        self.consumer_key = consumer_key
#        self.consumer_secret = consumer_secret
#        self.access_token = access_token
#        self.access_token_secret = access_token_secret

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creating the API object while passing in auth information
#    api = tweepy.API(auth, wait_on_rate_limit=True)
    api = tweepy.API(auth)

    stream = Stream(auth, l)
    #posts = api.user_timeline(screen_name="eafit",count=5,lang="en",tweet_mode="extended")
    #  Print the last 5 tweets
    print("Show the 5 recent tweets:\n")
    #i = 1
    #for tweet in posts[:5]:
        #print(str(i) + ') ' + tweet.full_text + '\n')
        #i = i+1
    stream.filter(track=['quinterocalle'])
