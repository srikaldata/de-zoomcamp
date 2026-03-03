"""REST API source for NYC taxi data (Data Engineering Zoomcamp API)."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/"
"""Base URL for the Zoomcamp NYC taxi API."""


@dlt.source
def nyc_taxi_rest_api_source():
    """Define dlt resources from the NYC taxi REST API (paginated JSON, 1000 records per page)."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": BASE_URL,
        },
        "resources": [
            {
                "name": "taxi_trips",
                "endpoint": {
                    "path": "data_engineering_zoomcamp_api",
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "base_page": 1,
                        "total_path": None,
                        "stop_after_empty_page": True,
                    },
                    # Response is a root-level JSON array; omit data_selector so the whole body is used
                },
            },
        ],
    }
    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(nyc_taxi_rest_api_source())
    print(load_info)  # noqa: T201
