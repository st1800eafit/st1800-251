# sudo apt install python3-pip
# sudo pip install pykafka
from pykafka import KafkaClient
client = KafkaClient(hosts="localhost:9092")
client.topics
topic = client.topics['sample-topic']
print(topic)
