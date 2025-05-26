# sudo apt install python3-pip
# sudo pip install kafka-python
from kafka import KafkaProducer
from kafka import KafkaClient
#client = KafkaClient(bootstrap_servers='localhost:9092')
#client.add_topic('sampletopic')
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('sample-topic', b'Hello, World!')
future = producer.send('sample-topic', key=b'message-two', value=b'This is Kafka-Python')
producer.flush()

