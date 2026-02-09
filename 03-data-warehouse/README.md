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
