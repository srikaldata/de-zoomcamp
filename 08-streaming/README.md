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


```
Q 4 to 6 preparation:
> docker exec -it workshop-postgres-1 psql -U postgres -d postgres

>> CREATE TABLE q4 (window_start TIMESTAMP(3), PULocationID INT, num_trips BIGINT, PRIMARY KEY (window_start, PULocationID));
CREATE TABLE q5 (window_start TIMESTAMP(3), PULocationID INT, num_trips BIGINT, PRIMARY KEY (window_start, PULocationID));
CREATE TABLE q6 (window_start TIMESTAMP(3), total_tip DOUBLE PRECISION, PRIMARY KEY (window_start));

>> \dt
List of relations
Schema | Name | Type | Owner 
--------+------+-------+----------
public | q4 | table | postgres
public | q5 | table | postgres
public | q6 | table | postgres
(3 rows)

```
