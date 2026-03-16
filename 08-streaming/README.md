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


# QUESTION 4 - tumbling window pickup location with highest trips
```
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q4.py

docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "SELECT PULocationID, num_trips FROM q4 ORDER BY num_trips DESC LIMIT 3;"
pulocationid | num_trips 
--------------+-----------
74 | 15
74 | 14
74 | 14
(3 rows)
```
* pulocationid = __74__ 


# QUESTION 5 - session window longest streak
```
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q5.py

docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "SELECT num_trips FROM q5 ORDER BY num_trips DESC LIMIT 1;"
num_trips 
-----------
81
(1 row)
```
ANSWER:
* __81 trips__


# QUESTION 6 - tumbling window largest tip
```
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q6.py

docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
SELECT window_start, total_tip 
FROM q6 
ORDER BY total_tip DESC 
LIMIT 10;"
window_start | total_tip 
---------------------+--------------------
2025-10-16 18:00:00 | 510.8599999999999
2025-10-30 16:00:00 | 494.41
2025-10-09 18:00:00 | 472.01000000000016
2025-10-10 17:00:00 | 470.0800000000002
2025-10-16 17:00:00 | 445.01000000000005
2025-10-02 17:00:00 | 439.5400000000001
2025-10-22 18:00:00 | 428.78000000000003
2025-10-29 17:00:00 | 426.7500000000001
2025-10-03 18:00:00 | 425.14000000000004
2025-10-23 17:00:00 | 412.6600000000001
(10 rows)

```
ANSWER:
* __2025-10-16 18:00:00__ with the largest tip of approximately 510.86 dollars
