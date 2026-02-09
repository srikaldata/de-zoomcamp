# SETUP
```
-- creating an external table
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.external_yellow_taxi_2024`
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://de_zoomcamp_data_warehouse_hw_2026/yellow_tripdata_2024-*.parquet']
)
```

```
-- creating a regular table
CREATE OR REPLACE TABLE `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`
AS
SELECT * FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.external_yellow_taxi_2024`;
```


# QUESTION 1: Counting records
```
-- QUESTION 1: count of records for the 2024 Yellow Taxi Data
SELECT COUNT(*) AS total_records_yellow_2024_janjune 
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`;
```
* ANSWER: 20332093


# QUESTION 2: Data Read Estimation
* estimated amount of data read when performing a query on external and regular tables
```
-- QUESTION 2: estimated amount of data read when performing a query on external and regular tables

-- external table query
SELECT COUNT(DISTINCT PULocationID) AS distinct_puid_external
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.external_yellow_taxi_2024`;

-- regular table query
SELECT COUNT(DISTINCT PULocationID) AS distinct_puid_regular
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`;
```
ANSWER:
* for external table:
    * Estimated bytes processsed = 0 B
    * Bytes processed = 155.12 MB 
* for regular table:
    * Estimated bytes processed = 155.12 MB
    * Bytes processed = 155.12 MB


# QUESTION 3: Understanding Columnar Storage
```
-- query to retrieve the PULocationID from the table (not the external table) in BigQuery. 
SELECT PULocationID 
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`;

-- query to retrieve the PULocationID and DOLocationID on the same table.
SELECT PULocationID, DOLocationID 
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`;
```

ANSWER:
* Estimated bytes processed for PULocation ID alone query = 155.12 MB
* Estimated bytes processed for PULocation ID and DOLocationID query = 310.24 MB
* REASON:
    * BigQuery is a columnar database, and it only scans the specific columns requested in the query. 
    * Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.


# QUESTION 4: Counting Zero Fare Trips
```
-- records having a fare_amount of 0
SELECT COUNT(*) AS num_trips_fare_zero 
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`
WHERE fare_amount = 0;
```
ANSWER:
* num_trips_fare_zero = 8333


# QUESTION 5: Partitioning And Clustering
```
-- new table with partition by date of dropoff and cluster by vendor id
CREATE OR REPLACE TABLE `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.paritioned_clustered_yellow_taxi_2024` 
PARTITION BY DATE(tpep_dropoff_datetime) 
CLUSTER BY VendorID AS 
SELECT * FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`;
```
ANSWER:
* Partition by tpep_dropoff_datetime and Cluster on VendorID
* REASON:
    * since the records are timeseries based, a partition on a time unit column which can be partitioned by less than 4000 partitions makes partitioning by tpep_dropoff_datetime (can also choose pickup) as the best option. 
    * we can choose the granularity of the partition to be date or month or year depending on the data at scale
    * The vendor ID is the main category across which the data in each partition can be clustered. 
    * Also, since the sorting order is in the same order of partition by order an overarching categorical column such as Vendor ID is a good starting point to form clusters.


# QUESTION 6: Partition Benefits (estimated bytes processed: regular v/s partitioned+clustered)
```
-- distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
-- using materialized (regular) table
SELECT DISTINCT VendorID
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';

-- using partitioned and clustered table
SELECT DISTINCT VendorID
FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.paritioned_clustered_yellow_taxi_2024`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';
```
ANSWER:
* Estimated bytes processed:
    * for materialized / regular table = 310.24 MB
    * for partitioned & clustered table = 26.84 MB
* REASON: partition pruning, helps filter the data quickly and efficiently


# QUESTION 7: External Table Storage
* we have uploaded the dataset in reference to GCP storage bucket
* the external table has been created referring the uri of the GCP storage bucket
* Thus, the data stored in external table persists in the GCP storage bucket


# QUESTION 8: Clustering Best Practices
* It is best practice in Big Query to always cluster your data:
* ANSWER:False
* REASON: 
    * USE CLUSTERING IF
        * If your partitions are really small (less than 1GB) OR your column has a high level of granularity 
        * If partitions are large number beyond limit of partition table (4000 partitions for GCP)
        * If partitions causes many changes and lots of modifications quite frequently


# QUESTION 9: Understanding table Scans
```
-- SELECT count(*) query FROM the materialized table you created
SELECT COUNT(*) FROM `de-zoomcamp-sri-2026.nyctaxiyellow2024janjune.regular_yellow_taxi_2024`;
``` 
* ANSWER: 
    * Estimated bytes processed = 0 B
    * REASON:
        * because BigQuery being a warehouse, already has metadata of the number of records in the materialized / regular table.
        * so no minimal to no processing is needed to display the metadata cached: number of records in the table as the result of this query
        * thus the estimated bytes processed shows as 0 bytes
