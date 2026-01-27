import click
import pandas as pd
import pyarrow.parquet as pq
import requests  # Added for robust downloading
import os
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# Schema for the Zone Lookup CSV
ZONE_DTYPE = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for processing')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """Ingest Nov 2025 Green Taxi data and Zone Lookup into PostgreSQL."""
    
    # 1. Database Connection
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # --- TASK 1: Green Taxi (Download then Stream) ---
    taxi_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    local_parquet = "taxi_data.parquet"
    
    print(f"Downloading Green Taxi data from {taxi_url}...")
    
    # Download the file locally to bypass PyArrow filesystem errors
    r = requests.get(taxi_url, stream=True)
    with open(local_parquet, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Ingesting Green Taxi data into {target_table}...")

    # Open the LOCAL Parquet file for streaming
    parquet_file = pq.ParquetFile(local_parquet)
    
    first = True

    # Streaming batches to remain memory-efficient
    for batch in tqdm(parquet_file.iter_batches(batch_size=chunksize), total=parquet_file.metadata.num_row_groups):
        df_chunk = batch.to_pandas()

        if first:
            df_chunk.to_sql(name=target_table, con=engine, if_exists='replace', index=False)
            first = False
        else:
            df_chunk.to_sql(name=target_table, con=engine, if_exists='append', index=False)

    # Clean up local file to save container space
    os.remove(local_parquet)
    print(f"Successfully ingested Green Taxi data.")

    # --- TASK 2: Zone Lookup (CSV) ---
    zone_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    zone_table = "taxi_zones"
    
    print(f"Ingesting Zone Lookup from {zone_url}...")
    
    # Pandas read_csv handles URLs much better than PyArrow handles Parquet URLs
    df_zones = pd.read_csv(zone_url, dtype=ZONE_DTYPE)
    df_zones.to_sql(name=zone_table, con=engine, if_exists='replace', index=False)
    
    print(f"Successfully ingested {len(df_zones)} rows into {zone_table}.")

if __name__ == '__main__':
    run()