# Universidad EAFIT
# Curso Almacenamiento y Recuperación de Información (ST1800 & ST1801)

# HIVE

## TABLAS SENCILLAS EN HIVE

## 1 Conexión al cluster Hadoop via HUE en Amazon EMR

Hue Web (cada uno tiene su propio cluster EMR)

    http://ec2.compute-1.amazonaws.com:8888
    

Usuarios: (entrar como hadoop/*********)

    username: hadoop
    password: ********

## 2. Los archivos de trabajo hdi-data.csv y export-data.csv

```
/user/hadoop/datasets/onu
```

## 3. Gestión (DDL) y Consultas (DQL)

### cada uno deberá crear su propia BD:

    CREATE DATABASE usernamedb

### Crear la tabla HDI en Hive:
```
# tabla manejada por hive: /user/hive/warehouse
use usernamedb;
CREATE TABLE HDI (id INT, country STRING, hdi FLOAT, lifeex INT, mysch INT, eysch INT, gni INT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE

# se requiere cargar datos a la tabla asi:
# 
# copiando datos directamente hacia hdfs:///warehouse/tablespace/managed/hive/mydb.db/hdi

$ hdfs dfs -cp hdfs:///user/hadoop/datasets/onu/hdi-data.csv hdfs:///warehouse/tablespace/managed/hive/hadoopdb.db/hdi

#
# cargardo datos desde hive:

## darle primero permisos completos al directorio:
## hdfs dfs -chmod -R 777 /user/hadoop/datasets/onu/

$ load data inpath '/user/hadoop/datasets/onu/hdi-data.csv' into table HDI

# tabla externa en hdfs: 
use usernamedb;
CREATE EXTERNAL TABLE HDI (id INT, country STRING, hdi FLOAT, lifeex INT, mysch INT, eysch INT, gni INT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION '/user/hadoop/datasets/onu2/hdi/'

# tabla externa en S3: 
use usernamedb;
CREATE EXTERNAL TABLE HDI (id INT, country STRING, hdi FLOAT, lifeex INT, mysch INT, eysch INT, gni INT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION 's3://emontoyadatalake/datasets/onu2/hdi/'

```

Nota: Esta tabla la crea en una BASE DE DATOS 'mydb'
```
use usernamedb;
show tables;
describe hdi;
```

### hacer consultas y cálculos sobre la tabla HDI:
```
select * from hdi;

select country, gni from hdi where gni > 2000;    
```

### EJECUTAR UN JOIN CON HIVE:

### Obtener los datos base: export-data.csv

usar los datos en 'datasets' de este repositorio.

### Iniciar hive y crear la tabla EXPO:

```
use usernamedb;
CREATE EXTERNAL TABLE EXPO (country STRING, expct FLOAT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION 's3://emontoyadatalake/datasets/onu2/export/'
```

### EJECUTAR EL JOIN DE 2 TABLAS:
```
SELECT h.country, gni, expct FROM HDI h JOIN EXPO e ON (h.country = e.country) WHERE gni > 2000;
```

## 4. WORDCOUNT EN HIVE:
```
use usernamedb;
CREATE EXTERNAL TABLE docs (line STRING) 
STORED AS TEXTFILE 
LOCATION 'hdfs://localhost/user/hadoop/datasets/gutenberg-small/';

--- alternativa2:
CREATE EXTERNAL TABLE docs (line STRING) 
STORED AS TEXTFILE 
LOCATION 's3://emontoyadatalake/datasets/gutenberg-small/';
```

// ordenado por palabra
```
SELECT word, count(1) AS count FROM (SELECT explode(split(line,' ')) AS word FROM docs) w 
GROUP BY word 
ORDER BY word DESC LIMIT 10;
```
// ordenado por frecuencia de menor a mayor
```
SELECT word, count(1) AS count FROM (SELECT explode(split(line,' ')) AS word FROM docs) w 
GROUP BY word 
ORDER BY count DESC LIMIT 10;
```

### RETO:

¿cómo llenar una tabla con los resultados de un Query? por ejemplo, como almacenar en una tabla el diccionario de frecuencia de palabras en el wordcount?

# 5. Apache Sqoop (opcional-adicional)

## PARA SQOOP DESDE HUE EN EMR-AMAZON tener en cuenta: 

sqoop-hue-settings [settings-emr.txt](settings-emr.txt)

## Datos en MySQL (crear previamente la base de datos en Amazon RDS/MySql)

scripts para gestionar y crear las tablas de 'cursosdb' y 'retail_db': [scripts-rdbms](rdbms/)

### instale una base de datos mysql en AWS RDS, y cree las 2 bases de datos de trabajo para este ejercicio.
### actualice los valos de 172.31.x.y a los valores reales donde instanciará la base de datos.

```
En 172.31.x.y, se tiene Mysql con (actualice la IP con el valor real de acuerdo a su contexto):
Base de datos: “cursodb”
Tabla: “employee” (ya existe una table llamada 'employee')
User: curso/curso
$ mysql –u curso -h 172.31.x.y –p
Enter password: ******
mysql> use cursodb;
mysql> show tables;
```

## comandos Sqoop desde Hue

conectarse a HUE, Menu: Query / Sqoop 1

todos los comandos no incluye 'sqoop'

import --connect jdbc:mysql://172.31.x.y:3306/cursodb 
--username curso --password ***** 
--table employee 
--target-dir /user/hadoop/employee -m 1

## Comandos Sqoop desde CLI

### ejecute el comando sqoop desde el nodo master del cluster EMR:

//Transferir UNA TABLA de una base de datos (tipo mysql) hacia HDFS:
```
$ hdfs dfs -rm -R /user/hadoop/employee
$ sqoop import --connect jdbc:mysql://172.31.x.y:3306/cursodb --username curso --password curso --table employee --target-dir /user/hadoop/employee -m 1
$ hdfs dfs -ls /user/hadoop/employee
$ hdfs dfs -cat /user/hadoop/employee/part-m-00000
```

//Transferir TODAS LAS TABLA de una base de datos (tipo mysql) hacia HDFS:
```
$ hdfs dfs -rm -R /user/hadoop/cursodb
$ sqoop import-all-tables --connect jdbc:mysql://172.31.x.y:3306/cursodb --username curso --password curso --warehouse-dir /user/hadoop/cursodb -m 1
$ hdfs dfs -ls -R /user/hadoop/cursodb
$ hdfs dfs -cat /user/hadoop/cursodb/employee/part-m-00000
```

// Crear tabla HIVE a partir de definición tabla Mysql:
```
$ sqoop create-hive-table --connect jdbc:mysql://172.31.x.y:3306/cursodb --username curso --password curso --table employee --hive-database username_cursodb --hive-table employee
```

// Transferir UNA TABLA de una base de datos (tipo mysql) hacia HIVE:

```
$ sqoop import --connect jdbc:mysql://172.31.x.y:3306/cursodb --username curso --password curso --table employee --hive-database username_cursodb --hive-import  --hive-table employee --hive-overwrite -m 1
```

// Transferir TODAS LAS TABLAS de una base de datos (tipo mysql) hacia HIVE:

```
PRIMERA VEZ:

$ sqoop import-all-tables --connect jdbc:mysql://172.31.x.y:3306/cursodb --username=curso --password=curso  --hive-database username_cursodb --create-hive-table --hive-import -m 1

SEGUNDA VEZ O INCREMENTAL (ya tabla creada):

$ sqoop import-all-tables --connect jdbc:mysql://172.31.x.y:3306/cursodb --username=curso --password=curso  --hive-database username_cursodb --hive-import --hive-overwrite -m 1

```

// Poblar o llenar la tabla Hive Manualmente:
```
$ beeline
> use usernamedb;
> CREATE TABLE username_emps (empid INT, name  STRING, salary INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  LINES TERMINATED BY '\n' STORED AS TEXTFILE;
>
```
// Cargar datos a Hive Manualmente:
```
> load data inpath '/user/hadoop/employee/part-m-00000' into table usernamedb.username_emps;
OK                          
> select * from username_emps;
OK
101 name1 1800
102 name2 1500
103 name3 1000
104 name4 2000
105 name5 1600
taken: 0.269 seconds, Fetched: 5 row(s) Time
> 
```

//Sqoop export hacia mysql:

// Crear una Tabla 'username_employee2' en Mysql con los mismos atributos de 'username_employee'
```
mysql> USE cursodb;
mysql> CREATE TABLE username_employee2 (  emp_id INT NOT NULL,  name VARCHAR(45),  salary INT,  PRIMARY KEY (emp_id));
```

// Asumiendo datos separados por ”,” en HDFS en:

/user/hadoop/mysql_in/*

```
$ sqoop export --connect jdbc:mysql://172.31.x.y:3306/cursodb --username curso -P --table username_employee2 --export-dir /user/hadoop/mysqlOut
```

## 6. MySQL vs Hive

### consulta hecha en MySQL de Promedio de salario de Empleados:

    $ mysql -u -h 172.31.x.y curso -p
    password: *****
    mysql> use cursodb;
    mysql> select AVG(salary) from employee;
    +-------------+                                                                    
    | AVG(salary) |                                                                    
    +-------------+                                                                    
    |   1580.0000 |                                                                    
    +-------------+                                                                    
    1 row in set (0.00 sec)                                                            
                                                                                   
    mysql>

### consulta hecha en HIVE de Promedio de salario de Empleados:

    Via HUE-Web> 

    # crear la tabla externa:

    use usernamedb;

    create external table employee (emp_id int, name string, salary float) 
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','  
    LINES TERMINATED BY '\n' 
    STORED AS textfile;

    select * from employee;

    select AVG(salary) from employee;