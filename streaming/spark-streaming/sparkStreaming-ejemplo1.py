import os
import findspark
from pyspark.sql.functions import explode, split, col
from pyspark.sql import SparkSession

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-amazon-corretto.x86_64"
os.environ["SPARK_HOME"] = "/home/ec2-user/spark-3.5.5-bin-hadoop3"

findspark.init()

# 1. Initialize Spark session
spark = SparkSession \
        .builder \
        .appName("testApp") \
        .getOrCreate()

# 2. Define a streaming DataFrame that reads from a socket

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# 3. Split each line into words and explode into individual rows

words = lines.select(
    explode(
        split(col("value"), " ")
    ).alias("word")
)

# 4. Count each unique word in the stream
wordCounts = words.groupBy("word").count()

# 5. Set up the output query to print word counts
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

# 6. Waiting input to process and output

query.awaitTermination()