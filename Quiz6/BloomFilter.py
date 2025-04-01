import base64

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BooleanType

spark = SparkSession.builder \
    .appName("BadWordDetection") \
    .getOrCreate()

spark_context = spark.sparkContext

# Loading the data from Hadoop
encoded_data = spark_context.textFile("hdfs:///user/jackson_adkins/quiz6/bit_vector_base64.txt").first()

bloom_filter_bytes = base64.b64decode(encoded_data)
bloom_filter = list(bloom_filter_bytes)

#Hash func for filter indexing
def compute_hash(word):
    return hash(word) % len(bloom_filter)

#check if line contains no bad words
def line_is_clean(text):
    words = text.split()
    return all(bloom_filter[compute_hash(word)] == 0 for word in words)

is_clean_udf = udf(line_is_clean, BooleanType())

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

filtered_lines = lines.filter(is_clean_udf(col("value")))

query = filtered_lines.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()