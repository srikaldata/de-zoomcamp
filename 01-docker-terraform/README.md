# QUESTION 1 - Understanding docker images


* get the image automatically and run the python:3.13 container

`docker run -it --rm --entrypoint bash python:3.13`

* inside the container find the version of pip

`pip --version`

OUTPUT:
```
/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

# QUESTION 2 - Understanding docker networking and docker-compose

* the hostport:internalport of the 'db' service is ports: - '5433:5432'
* which means any internal services within the docker network will use port 5432 to connect to the 'db' service 

* So, the hostname and port that pgadmin should use to connect to the postgres database is `db:5432`

# QUESTION 3 - Counting short trips

```
SELECT COUNT(*) AS total_trips_under_1_mile
FROM public.green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01' 
	AND lpep_pickup_datetime <= '2025-12-01'
	AND trip_distance <= 1
;
```
OUTPUT: <br>
8007

# QUESTION 4 - Longest trip for each day
```
SELECT DATE(lpep_pickup_datetime) AS max_trip_dist_day
FROM public.green_taxi_data
WHERE trip_distance <= 100
ORDER BY trip_distance DESC
LIMIT 1
;
```
OUTPUT: <br>
2025-11-14

# QUESTION 5 - Biggest pickup zone
```
SELECT DATE(t.lpep_pickup_datetime), zpu."Zone" AS pickup_zone, SUM(t.total_amount) AS zone_total_amount
FROM public.green_taxi_data AS t
JOIN public.taxi_zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY 1, 2
ORDER BY zone_total_amount DESC
LIMIT 1;
```
OUTPUT: <br>
"2025-11-18"	"East Harlem North"	9281.920000000004

# QUESTION 6 - Largest tip
```
SELECT zdo."Zone" AS dropoff_zone, MAX(t.tip_amount) AS zone_max_tip_amount
FROM public.green_taxi_data AS t
JOIN public.taxi_zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN public.taxi_zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE zpu."Zone" = 'East Harlem North'
GROUP BY 1
ORDER BY zone_max_tip_amount DESC
LIMIT 1;
```
OUTPUT: <br>
"Yorkville West"	81.89
