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
