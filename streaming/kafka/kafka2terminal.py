# sudo apt install python3-pip
# sudo pip install kafka-python
import json
from kafka import KafkaConsumer

# topic's name
KAFKA_TOPIC = "tweets_topic"

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers='localhost:9092')

for message in consumer:

    try:
        # Decode the JSON from Twitter
        datajson = json.loads(message)

        # grab the 'created_at' data from the Tweet to use for display
        created_at = datajson['created_at']

        # print out a message to the screen that we have collected a tweet
        print("Tweet collected at " + str(created_at))

    except Exception as e:
        print(e)
