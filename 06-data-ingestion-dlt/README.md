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
