from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()
sc = spark.sparkContext

files = sc.textFile("s3://emontoyadatalake/datasets/gutenberg-txt-es/*.txt")
wc = files.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
wc.coalesce(1).saveAsTextFile("hdfs:///tmp/wcout1")
