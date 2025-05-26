# Universidad EAFIT
# Curso st1800 Sistemas Intensivos en Datos, 2024-2
# Profesor: Edwin Montoya M. – emontoya@eafit.edu.co

# Laboratorio Apache Kafka / flink en EC2

## alcance:

### 1. instalar apache kafka en una VM EC2
###  gestión de tópicos desde cli
###  ejecución de al menos 2 producers desde cli
###  ejecución de al menos 2 consumers desde cli
###  ejecutar y entender producers y consumers en python
### 2. RETO: Crear un agente logstream o clickstream hacia kafka  y procesado con flink o spark stream

## 1. instalar apache kafka en una VM EC2

Crear una VM linux o en su PC 

Instalar java y Kafka: 

        $ sudo apt install default-jdk

        $ wget https://downloads.apache.org/kafka/3.8.1/kafka_2.12-3.8.1.tgz

        $ tar -xzf kafka_2.12-3.8.1.tgz

        $ cd kafka_2.12-3.8.1

Editar los archivos: 

        $ vim config/zookeeper.properties 

Actualizar la variable: (lo puede dejar en el /tmp) 

        dataDir=/tmp/zookeeper 

a: 

        dataDir=/home/ubuntu/zookeeper 


        $ vim config/server.properties 

Actualizar la variable: o tener en cuenta donde deja los logs en el /tmp 

        log.dirs=/tmp/kafka-logs 

a: 

        dataDir=/home/ubuntu/kafka-logs 

 Iniciar zookeeper: 

        $ bin/zookeeper-server-start.sh -daemon config/zookeeper.properties 

Iniciar el servidor de Kafka: 

      $ bin/kafka-server-start.sh -daemon config/server.properties 

crear un tópico: 

        $ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sample-topic

Listar los tópicos: 

        $ bin/kafka-topics.sh  --list --bootstrap-server localhost:9092

Borrar un tópico: 

        $ bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic sample-topic 

PRODUCERS: 

        $ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic sample-topic 

CONSUMERS: 

        $ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sample-topic --from-beginning 

## ejecución de programas en python para producir y consumir mensajes con Apache kafka:

### instalar la libreria de kafka en python:

        $ sudo apt install python3-pip
        $ sudo pip install kafka-python

### ejecutar ejemplo

1. abrir una consola para consumidor1:

        $ cd st1800-242/streaming/kafka
        $ python3 kafka-consumer-localhost.py

2. abrir una segunda consola para consumidor2:

        $ cd st1800-242/streaming/kafka
        $ python3 kafka-consumer-localhost.py

3. abrir una tercera consola para productor1:

        $ cd st1800-242/streaming/kafka
        $ python3 kafka-producer-localhost.py

enviar algunos mensajes de prueba

4. abrir una cuarta consola para productor2:

        $ cd st1800-242/streaming/kafka
        $ python3 kafka-producer-localhost.py

enviar algunos mensajes de prueba

// listo!!!!

Detener el servidor de Kafka: 

        $ bin/kafka-server-stop.sh 

Detener zookeeper: 

      $ bin/zookeeper-server-stop.sh  

## 2. RETO: Crear un agente logstream o clickstream hacia kafka con un procesador de flujo muy sencillo en apache flink o spark stream con salida a pantalla (printout)
