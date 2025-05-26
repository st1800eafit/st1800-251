import os
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, current_timestamp, window

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-amazon-corretto.x86_64"
os.environ["SPARK_HOME"] = "/home/ec2-user/spark-3.5.5-bin-hadoop3"

findspark.init()

# 1. Initialize Spark session
spark = SparkSession \
    .builder \
    .appName("testApp") \
    .getOrCreate()

# 2. Leer desde socket
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# 3. Extraer palabras
words = lines.select(
    explode(
        split(col("value"), " ")
    ).alias("word")
)

# 4. Agregar timestamp
words = words.withColumn("timestamp", current_timestamp())

# 5. Agregar watermark y agrupar por ventana
wordCounts = words \
    .withWatermark("timestamp", "10 seconds") \
    .groupBy(
        window(col("timestamp"), "10 seconds"),
        col("word")
    ) \
    .count()

# 6. Escritura a archivos CSV
query = wordCounts \
    .writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "output/word_counts") \
    .option("checkpointLocation", "output/checkpoints") \
    .start()

# 7. Esperar por entrada de datos para procesar y enviar a salida

query.awaitTermination()