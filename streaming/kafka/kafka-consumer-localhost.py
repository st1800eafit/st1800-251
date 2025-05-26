# sudo apt install python3-pip
# sudo pip install kafka-python
from kafka import KafkaClient
from kafka import KafkaConsumer
consumer = KafkaConsumer('sample-topic',bootstrap_servers='localhost:9092')
for message in consumer:
    print (message)
