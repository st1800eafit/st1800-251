# pip install kafka-python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaClient
#from kafka import SimpleProducer, KafkaClient
from kafka import KafkaConsumer, KafkaProducer

import mytwitterKeys

consumer_key = mytwitterKeys.CONSUMER_KEY
consumer_secret = mytwitterKeys.CONSUMER_SECRET
access_token = mytwitterKeys.ACCESS_TOKEN
access_token_secret = mytwitterKeys.ACCESS_TOKEN_SECRET

producer = KafkaProducer(bootstrap_servers='b-1.st1612-cluster-1.e0djg5.c8.kafka.us-east-1.amazonaws.com:9092')
producer.send('AWSKafkaTutorialTopic', b'Hello, World!')
producer.send('AWSKafkaTutorialTopic', key=b'message-two', value=b'This is Kafka-Python')

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("trump", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

#kafka = KafkaClient("b-1.st1612-cluster-1.e0djg5.c8.kafka.us-east-1.amazonaws.com:9092")
#producer = SimpleProducer(kafka)
#l = StdOutListener()
#auth = OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#stream = Stream(auth, l)
#stream.filter(track="trump")

