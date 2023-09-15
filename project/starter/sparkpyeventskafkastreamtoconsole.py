from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, unbase64, base64, split
from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType

# TO-DO: using the spark application object, read a streaming dataframe from the Kafka topic stedi-events as the source
# Be sure to specify the option that reads all the events from the topic including those that were published before you started the spark stream
spark = SparkSession.builder.appName("stedi-human-balance").getOrCreate()
spark.sparkContext.setLogLevel("WARN")
stedi_events_df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:19092")
    .option("subscribe", "stedi-events")
    .option("startingOffsets", "earliest")
    .load()
)
                                   
# TO-DO: cast the value column in the streaming dataframe as a STRING
stedi_events_df = stedi_events_df.selectExpr("cast(key as string) key", "cast(value as string) value")

# TO-DO: parse the JSON from the single column "value" with a json object in it, like this:
customer_json_schema = StructType(
    [
        StructField("customer", StringType()),
        StructField("score", StringType()),
        StructField("riskDate", DateType()),
    ]
)

(
    stedi_events_df
    .withColumn("value", from_json("value", customer_json_schema))
    .select(col("value.*"))
    .createOrReplaceTempView("CustomerRisk")
)
# +------------+
# | value      |
# +------------+
# |{"custom"...|
# +------------+
#
# and create separated fields like this:
# +------------+-----+-----------+
# |    customer|score| riskDate  |
# +------------+-----+-----------+
# |"sam@tes"...| -1.4| 2020-09...|
# +------------+-----+-----------+
#
# storing them in a temporary view called CustomerRisk
# TO-DO: execute a sql statement against a temporary view, selecting the customer and the score from the temporary view, creating a dataframe called customerRiskStreamingDF
# TO-DO: sink the customerRiskStreamingDF dataframe to the console in append mode
customerRiskStreamingDF = spark.sql("select customer, score from CustomerRisk")
customerRiskStreamingDF.writeStream.outputMode("append").format("console").start().awaitTermination()
# 
# It should output like this:
#
# +--------------------+-----
# |customer           |score|
# +--------------------+-----+
# |Spencer.Davis@tes...| 8.0|
# +--------------------+-----
# Run the python script by running the command from the terminal:
# /home/workspace/submit-event-kafka-streaming.sh
# Verify the data looks correct 