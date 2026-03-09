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


