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

`Spark version: 4.1.1`

# QUESTION 2 - size of file repartitioned 4 times
In jupyter nb:
```
df.repartition(4).write.mode('overwrite').parquet('data/repartitioned_taxi')
```

In CLI:

`cd /data/repartitioned_taxi`

`ls -lh`

ANSWER:
* 25 M

# QUESTION 3 - trip count 
```
df.filter(F.to_date(df.tpep_pickup_datetime) == "2025-11-15").count()
```

ANSWER:
* 162604 trips

# QUESTION 4 - longest trip
