INSTRUCTIONS TO RUN LOCALLY:
* profiles.yml needs to be inside <username>/.dbt/ in windows machines
* execute ingest_data.py for ingesting green and yellow taxi data
* execute ingest_data_fhv.py for ingesting fhv data
* no need to run > dbt init
* need to run > dbt deps before running or building models
* use --full-refresh flags when needed
* to start building from scratch use > dbt clean to purge and build / run again
* for OOM issues during build use > dbt retry to continue from where it is left off
* make sure dbt profiles.yml memory allocation is tweaked based on the system that runs dbt 
* to run UI from the duckDB.exe open the exe file and in the command line run > INSTALL ui; LOAD ui; Run CALL start_ui();
* to run UI from command line run > duckdb -ui

# QUESTION 1 - dbt lineage and execution
* If you run dbt run --select int_trips_unioned, what models will be built?
* ANSWER:
    * int_trips_unioned only
* REASON:
    * since dbt run is performed to select only the model without upstream / downstream dependencies
    * also, the existence of a ref pointing to the staging table modelsdoes not automatically force dbt to build the parent models during a run.


# QUESTION 2 - dbt tests
* Your model fct_trips has been running successfully for months. (existing list of accepted_values --> [1, 2, 3, 4, 5])  A new value 6 now appears in the source data.
* ANSWER:
    * dbt will fail the test, returning a non-zero exit code
    * because the number 6 is not in the accepted values list


# QUESTION 3 - counting records in fct_monthly_zone_revenue
```
SELECT COUNT(*) AS num_records 
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue;
```
* OUTPUT:
    * 12184 records


# QUESTION 4 - best performing zone for green taxis (2020)
```
-- top 5 best performing zones for green taxis in year 2020
SELECT 
    pickup_zone, 
    SUM(revenue_monthly_total_amount) AS total_revenue
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue 
WHERE service_type = 'Green' AND YEAR(revenue_month) = 2020 
GROUP BY pickup_zone 
ORDER BY total_revenue DESC 
LIMIT 5;
```
* ANSWER:
    * East Harlem North = 1817302.95


# QUESTION 5 - green taxi trip counts (october 2019)
```
SELECT 
    SUM(total_monthly_trips) AS total_october_2019_trips 
FROM taxi_rides_ny.prod.fct_monthly_zone_revenue 
WHERE service_type = 'Green' AND revenue_month = '2019-10-01'; 
-- revenue_month's month and year need not be parsed using functions since it has only 1st day of all months even though it is in DATE format
```
* OUTPUT:
    * 384624 trips


