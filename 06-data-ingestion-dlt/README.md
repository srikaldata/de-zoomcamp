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
