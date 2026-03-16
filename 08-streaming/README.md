# QUESTION 1 - redpanda version
```$ docker exec -it workshop-redpanda-1 rpk version```

OUTPUT:
* rpk version: __v25.3.9__


# QUESTION 2 - sending data to redpanda
```
> docker exec -it workshop-redpanda-1 rpk topic create green-trips

> docker exec -it workshop-redpanda-1 rpk topic list
NAME PARTITIONS REPLICAS
green-trips 1 1

> uv run src/producers/producer.py
Downloading dataset...
Starting production to green-trips...
took 11.99 seconds
```

ANSWER:
* __11.99 seconds__ --> approximately 10 seconds


# QUESTION 3 - trips with distance greater than 5 km 
```
> uv run src/consumers/consumer.py
Counting trips with distance > 5.0 green-trips...
Processed 10000 rows...
Processed 20000 rows...
Processed 30000 rows...
Processed 40000 rows...

--- Result ---
Total trips processed: 49416
Trips with distance > 5.0: 8506
```

ANSWER:
* Trips with distance > 5.0: __8506__

