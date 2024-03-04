from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Spark Job")\
        .getOrCreate()

data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]
df = spark.createDataFrame(data)
df.show()

spark.stop()