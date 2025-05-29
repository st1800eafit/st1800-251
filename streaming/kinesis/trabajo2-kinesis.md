# Universidad EAFIT
# Módulo: Arquitectura Streaming con AWS
# Profesor: Edwin Montoya M. – emontoya@eafit.edu.co

# Amazon Kinesis Lab

# Trabajo 2 - parte 1 - Logs Agent -> Kinesis Firehose -> S3 -> Glue -> Athena:

1. crear un servicio kinesis firehose por la consola web:

        Create: Amazon Data Firehouse
        
        Source: Direct PUT
        Destination: Amazon S3

        Delivery stream name: purchaseLogs

        Destination settings/S3 bucket: st1800orderlogs     (escoja su propio nombre de bucket y realice todas las actualizaciones pertinentes)
        
        Buffer hints, compression and encryption:
        Buffer interval: 60 segs

        Advanced settings:
        PermissionsInfo:
        (o) Choose existing IAM role: LabRole

        Click on: Create Firehose stream
        
2. crear una instancia EC2 AMI 2023 linux

Actualizar el IAM Role a 'LabInstanceProfile'

Este Role asociarlo a la instancia EC2 donde instalará el agent de kinesis.

[seguir-estas-instrucciones](instalar-vm-agente.txt)

3. instalar el agente kinesis

[seguir-estas-instrucciones](instalar-vm-agente.txt)

4. descargar los logs (OnlineRetail.csv) ejemplo y LogsGenerator.py (ya estan en el github)

## Nota: antes de Generar Logs, descomprima el archivo: OnlineRetail.csv.gz

        $ cd kinesis/OrderHistory
        $ gunzip OnlineRetail.csv.gz

5. cambiar permisos, crear directorios, etc:

        $ chmod a+x LogGenerator.py
        $ sudo mkdir /var/log/acmeco

### copie el archivo del repo github: agent.json-with-firehose hacia /etc/aws-kinesis/agent.json

        $ sudo cp agent.json-with-firehose /etc/aws-kinesis/agent.json

        $ sudo vim /etc/aws-kinesis/agent.json

6. iniciar el agente:

        $ sudo systemctl start aws-kinesis-agent

7. ejecutar un envio de logs:

        $ cd kinesis/OrderHistory

        $ sudo python3 LogGenerator.py 1000

8. chequee en unos minutos el 'bucket' st1800orderlogs o equivalente.

9. ejecute aws glue y consulte con aws athena los datos de S3 st1800orderlogs o equivalente.

# Trabajo 2 - parte 2 - Logs Agent -> Kinesis Data Streams -> Lambda -> DynamoDB:

1. Crear un Kinesis Data Stream en AWS:

        Create data Stream:
        name: acmecoOrders
        Boton: Create data Stream

2. crear la tabla DynamoDB

        Table Name: acmecoOrders
        Partition Key: CustomerID / Number
        Sort key - optional: OrderID / String
        Use defaults setting
        boton: Create table

3. Configurar el kinesis-agent para enviar los logs al Kinesis Data Stream

### copie el archivo del repo github: agent.json-with-firehose-and-datastreams hacia /etc/aws-kinesis/agent.json

        $ sudo cp agent.json-with-firehose-and-datastreams /etc/aws-kinesis/agent.json

        $ sudo more /etc/aws-kinesis/agent.json

        se adiciona al archivo original de firehose: 

           "flows": [
                {
                "filePattern": "/var/log/acmeco/*.log",
                "kinesisStream": "acmecoOrders",
                "partitionKeyOption": "RANDOM",
                "dataProcessingOptions": [
                        {
                        "optionName": "CSVTOJSON",
                        "customFieldNames": ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "Customer", "Country"]
                        }
                ]
                },

4. reiniciar el servicio:

        $ sudo systemctl restart aws-kinesis-agent

5. generar logs de prueba:

        $ sudo python3 LogGenerator.py 1000

6. ir a la instancia EC2 donde tenemos en kinesis-agent para consumirlos MANUALMENTE y almacenarlos en la base de datos DynamoDB

        $ sudo yum install -y python3-pip
        $ sudo pip3 install boto3

        actualizar las credenciales AWS en el linux

        $ mkdir .aws
        $ aws configure

Nota: Copy las credenciales de AWS ACADEMY en el archivo generado. tener en cuenta la region: us-east-1 y el formato: json

7. Configurar un Consumer del kinesis data stream, mediente un cliente standalone (Consumer.py)

Nota: tenga en cuenta que esta versión es python2, hay que adaptarlo a versión python3

        configurar 'Consumer.py'
        $ chmod a+x Consumer.py
        $ python3 Consumer.py

        en otra terminal, generar nuevos registros para que el consumer los adquiera de kinesis y los inserte en DynamoDB

8. Crear una funcion aws lambda para consumir de kinesis data streams e insertar en una tabla DynamoDB:

        Actualizar el IAM Role = 'LabRole'

        Crear la function lambda 'Author from scratch':
        Function name: ProcessOrders
        Runtime: python 3.9
        Use an existing role: LabRole
        
        Botón: create function

        +Add Trigger: Kinesis Data Stream
        Kinesis stream: kinesis/acmecoOrders

        inserte el código de: lambda-function.txt del github
        haga Deploy

9. chequear en la base de datos DynomoDB la inserción de los registros.