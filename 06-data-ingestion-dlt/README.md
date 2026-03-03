### setup commands
`uv init`

`uv add "dlt[workspace]"`

`uv run dlt init dlthub:taxi_pipeline duckdb`

### Prompting the agent in Cursor
```
Build a REST API source for NYC taxi data.

API details:
- Base URL: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
- Data format: Paginated JSON (1,000 records per page)
- Pagination: Stop when an empty page is returned

Place the code in taxi_pipeline.py and name the pipeline taxi_pipeline.
Use @dlt rest api as a tutorial.
```

* followed up error debugging and other operations with follow-up prompts

### Running the pipeline

`uv run python taxi_pipeline.py`

OUTPUT:

Pipeline taxi_pipeline load step completed in 3.69 seconds
1 load package(s) were loaded to destination duckdb and into dataset taxi_pipeline_dataset
The duckdb destination used duckdb:////home/.../06-data-ingestion-dlt/taxi-pipeline/taxi_pipeline.duckdb location to store data
Load package 1772492992.6037815 is LOADED and contains no failed jobs

### viewing the dlt pipeline stages
`uv run dlt pipeline taxi_pipeline show`

* checked and confirmed the pipeline stages at localhost:/####

### installing necessary packages for querying
`uv pip install pandas`

## Querying using marimo
`uv run marimo edit`

* runs at localhost:/####?access_token=####
* can query the table from here

### Attaching the database in marimo:
`ATTACH 'taxi_pipeline.duckdb' AS taxi_data;`


### Table details:
`SHOW ALL TABLES;`

OUTPUT:
| database | schema | name | column_names | column_types | temporary |
|---|---|---|---|---|---|
| taxi_data | taxi_pipeline_dataset | _dlt_loads | ["load_id","schema_name","status","inserted_at","schema_version_hash"] | ["VARCHAR","VARCHAR","BIGINT","TIMESTAMP WITH TIME ZONE","VARCHAR"] | false |
| taxi_data | taxi_pipeline_dataset | _dlt_pipeline_state | ["version","engine_version","pipeline_name","state","created_at","version_hash","_dlt_load_id","_dlt_id"] | ["BIGINT","BIGINT","VARCHAR","VARCHAR","TIMESTAMP WITH TIME ZONE","VARCHAR","VARCHAR","VARCHAR"] | false |
| taxi_data | taxi_pipeline_dataset | _dlt_version | ["version","engine_version","inserted_at","schema_name","version_hash","schema"] | ["BIGINT","BIGINT","TIMESTAMP WITH TIME ZONE","VARCHAR","VARCHAR","VARCHAR"] | false |
| taxi_data | taxi_pipeline_dataset | taxi_trips | ["end_lat","end_lon","fare_amt","passenger_count","payment_type","start_lat","start_lon","tip_amt","tolls_amt","total_amt","trip_distance","trip_dropoff_date_time","trip_pickup_date_time","surcharge","vendor_name","_dlt_load_id","_dlt_id","store_and_forward"] | ["DOUBLE","DOUBLE","DOUBLE","BIGINT","VARCHAR","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","TIMESTAMP WITH TIME ZONE","TIMESTAMP WITH TIME ZONE","DOUBLE","VARCHAR","VARCHAR","VARCHAR","DOUBLE"] | false |

### Table description:
`DESCRIBE taxi_data.taxi_pipeline_dataset.taxi_trips;`

OUTPUT:
| column_name | column_type | null | key | default | extra |
|---|---|---|---|---|---|
| end_lat | DOUBLE | YES |  |  |  |
| end_lon | DOUBLE | YES |  |  |  |
| fare_amt | DOUBLE | YES |  |  |  |
| passenger_count | BIGINT | YES |  |  |  |
| payment_type | VARCHAR | YES |  |  |  |
| start_lat | DOUBLE | YES |  |  |  |
| start_lon | DOUBLE | YES |  |  |  |
| tip_amt | DOUBLE | YES |  |  |  |
| tolls_amt | DOUBLE | YES |  |  |  |
| total_amt | DOUBLE | YES |  |  |  |
| trip_distance | DOUBLE | YES |  |  |  |
| trip_dropoff_date_time | TIMESTAMP WITH TIME ZONE | YES |  |  |  |
| trip_pickup_date_time | TIMESTAMP WITH TIME ZONE | YES |  |  |  |
| surcharge | DOUBLE | YES |  |  |  |
| vendor_name | VARCHAR | YES |  |  |  |
| _dlt_load_id | VARCHAR | NO |  |  |  |
| _dlt_id | VARCHAR | NO |  |  |  |
| store_and_forward | DOUBLE | YES |  |  |  |

### Total records
`SELECT COUNT(*) FROM taxi_data.taxi_pipeline_dataset.taxi_trips;`

OUTPUT:
10000
