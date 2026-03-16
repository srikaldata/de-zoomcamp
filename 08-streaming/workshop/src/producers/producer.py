import dataclasses
import json
import sys
import time
from pathlib import Path

# Fix pathing
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from kafka import KafkaProducer
from models import Ride, ride_from_row

# 1. Correct URL and ALL required columns
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
columns = [
    'lpep_pickup_datetime', 
    'lpep_dropoff_datetime', 
    'PULocationID', 
    'DOLocationID', 
    'passenger_count', 
    'trip_distance', 
    'tip_amount', 
    'total_amount'
]

print("Downloading dataset...")
df = pd.read_parquet(url, columns=columns) # Removed .head(1000) to process all rows

def ride_serializer(ride):
    # Ensure your Ride model converts datetimes to strings inside!
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')

server = 'localhost:9092'
producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=ride_serializer
)

# 2. Correct Topic Name
topic_name = 'green-trips'

print(f"Starting production to {topic_name}...")
t0 = time.time()

for _, row in df.iterrows():
    ride = ride_from_row(row)
    producer.send(topic_name, value=ride)
    # Removing time.sleep(0.01) and print() to get an accurate benchmark 
    # Printing 61k rows will significantly slow down your "time taken"

producer.flush()
t1 = time.time()

print(f'took {(t1 - t0):.2f} seconds')