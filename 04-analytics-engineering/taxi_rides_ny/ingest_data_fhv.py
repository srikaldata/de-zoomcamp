import duckdb
import requests
from pathlib import Path

# The base URL remains the same
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def download_and_convert_fhv():
    taxi_type = "fhv"
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    # We only need 2019 for FHV based on your requirements
    year = 2019
    
    for month in range(1, 13):
        parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
        parquet_filepath = data_dir / parquet_filename

        if parquet_filepath.exists():
            print(f"Skipping {parquet_filename} (already exists)")
            continue

        # Download CSV.gz file
        csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
        csv_gz_filepath = data_dir / csv_gz_filename
        
        # Note: The URL structure for FHV might be slightly different in the repo
        # If this fails, the taxi_type in the URL might need to be 'fhv'
        url = f"{BASE_URL}/{taxi_type}/{csv_gz_filename}"
        
        print(f"Downloading {csv_gz_filename}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(csv_gz_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Converting {csv_gz_filename} to Parquet...")
            con = duckdb.connect()
            # We use read_csv_auto which is usually good at handling the FHV schema
            con.execute(f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()

            # Remove the CSV.gz file to save space
            csv_gz_filepath.unlink()
            print(f"Completed {parquet_filename}")
            
        except requests.exceptions.HTTPError as e:
            print(f"Could not download {csv_gz_filename}: {e}")

if __name__ == "__main__":
    # 1. Download and convert FHV 2019
    download_and_convert_fhv()

    # 2. Load into DuckDB
    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS staging")

    print("Creating staging table for FHV...")
    con.execute(f"""
        CREATE OR REPLACE TABLE staging.fhv_tripdata AS
        SELECT * FROM read_parquet('data/fhv/*.parquet', union_by_name=true)
    """)
    
    # Quick count check
    count = con.execute("SELECT count(*) FROM staging.fhv_tripdata").fetchone()[0]
    print(f"Total records loaded into staging.fhv_tripdata: {count}")

    con.close()
