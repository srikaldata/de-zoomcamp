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
