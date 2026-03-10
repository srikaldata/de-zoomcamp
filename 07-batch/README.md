# QUESTION 1 - pyspark version
```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

print(f"Spark version: {spark.version}")
```

OUTPUT:

__`Spark version: 4.1.1`__

# QUESTION 2 - size of file repartitioned 4 times
In jupyter nb:
```
df.repartition(4).write.mode('overwrite').parquet('data/repartitioned_taxi')
```

In CLI:

`cd /data/repartitioned_taxi`

`ls -lh`

ANSWER:
* __25 MB__

# QUESTION 3 - trip count 
```
df.filter(F.to_date(df.tpep_pickup_datetime) == "2025-11-15").count()
```

ANSWER:
* __162604 trips__

# QUESTION 4 - longest trip
```
# creating a temp view to query using SQL
df.createOrReplaceTempView("yellow_taxi_trips")

spark.sql('\
    SELECT MAX(timestampdiff(SECOND, tpep_pickup_datetime, tpep_dropoff_datetime) / 3600.0) AS longest_trip_duration_hours \
    FROM yellow_taxi_trips;' ).show()
```

ANSWER:
* __90.6 hours__

# QUESTION 5 - spark app ui local server port
* it runs in the localhost in port 4040 (if no other apps are hosted on that port)

