# https://pythondata.com/collecting-storing-tweets-with-python-and-mongodb/

from __future__ import print_function
import tweepy
import json
from pykafka import KafkaClient

# rename twitter-keys-template.py to twitter-keys.py and update to real keys
import mytwitterKeys

client = KafkaClient(hosts="localhost:9092")

producer = KafkaProducer(bootstrap_servers='localhost:9092')
KAFKA_TOPIC = "tweets_topic"

topic = client.topics[KAFKA_TOPIC]

WORDS = ['quinterocalle', 'valledelsoftware']

CONSUMER_KEY = mytwitterKeys.CONSUMER_KEY
CONSUMER_SECRET = mytwitterKeys.CONSUMER_SECRET
ACCESS_TOKEN = mytwitterKeys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = mytwitterKeys.ACCESS_TOKEN_SECRET


class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.

            with topic.get_sync_producer() as producer:
                producer.produce(datajson)

        except Exception as e:
            print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
