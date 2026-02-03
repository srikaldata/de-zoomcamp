# QUESTION 1
* Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?
    * Non-scheduled workflow
    * Select taxi type = yellow
    * Select year = 2020
    * Select month = 12
    * go to Executions --> Outputs --> outputFiles -->  yellow_tripdata_2020-12.csv
    * ANSWER: 128.3 MiB

# QUESTION 2
* What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
    * Non-scheduled workflow
    * Select taxi type = yellow
    * Select year = 2020
    * Select month = 12
    * go to Executions --> Outputs --> outputFiles 
    * ANSWER: green_tripdata_2020-04.csv

# QUESTION 3
* How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
    * go to scheduled workflow --> Triggers --> yellow_schedule
    * Start = 2020-01-01 00:00:00
    * End = 2020-12-31 23:59:59
    * Select taxi type = yellow
    * go to pgadmin --> ny_taxi_server --> Databases --> ny_taxi --> Schemas --> public --> Tables --> yellow_tripdata
    * `SELECT COUNT(*) FROM yellow_tripdata`
    * ANSWER: 24648499

# QUESTION 4
* How many rows are there for the Green Taxi data for all CSV files in the year 2020?
    * go to scheduled workflow --> Triggers --> green_schedule
    * Start = 2020-01-01 00:00:00
    * End = 2020-12-31 23:59:59
    * Select taxi type = green
    * go to pgadmin --> ny_taxi_server --> Databases --> ny_taxi --> Schemas --> public --> Tables --> green_tripdata
    * `SELECT COUNT(*) FROM green_tripdata`
    * ANSWER: 1734051

# QUESTION 5
* How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
    * drop the existing yellow_tripdata table in postgreSQL from pgadmin
    * Non-scheduled workflow
    * Select taxi type = yellow
    * Select year = 2021
    * Select month = 03
    * go to pgadmin --> ny_taxi_server --> Databases --> ny_taxi --> Schemas --> public --> yellow_tripdata
    * `SELECT COUNT(*) FROM yellow_tripdata`
    * ANSWER: 1925152

# QUESTION 6
*  How would you configure the timezone to New York in a Schedule trigger?
    * we can use the timezone property in Schedule trigger 
    * specifying America/New_York or UTC-05:00 (standard time) or UTC-04:00 (daylight time) 
    * So to auto adapt across daylight savings and standard timezone the best way is to use America/New_York
    * For example:
```
triggers:
  - id: green_schedule_or_yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: America/New_York
```
