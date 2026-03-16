import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kafka import KafkaConsumer
from models import ride_deserializer

server = 'localhost:9092'
topic_name = 'green-trips'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='distance-counter-group',
    value_deserializer=ride_deserializer,
    consumer_timeout_ms=5000
)

print(f"Counting trips with distance > 5.0 {topic_name}...")

trip_count = 0
total_processed = 0

try:
    for message in consumer:
        ride = message.value
        total_processed += 1
        
        # The specific logic for Question 3
        if ride.trip_distance > 5.0:
            trip_count += 1
            
        if total_processed % 10000 == 0:
            print(f"Processed {total_processed} rows...")

except Exception as e:
    print(f"Error: {e}")

finally:
    print("\n--- Result ---")
    print(f"Total trips processed: {total_processed}")
    print(f"Trips with distance > 5.0: {trip_count}")
    consumer.close()

"""
count = 0
for message in consumer:
    ride = message.value
    pickup_dt = ride.lpep_pickup_datetime
    print(f"Received: PU={ride.PULocationID}, DO={ride.DOLocationID}, "
          f"distance={ride.trip_distance}, amount=${ride.total_amount:.2f}, "
          f"pickup={pickup_dt}")
    count += 1
    if count >= 10:
        print(f"\n... received {count} messages so far (stopping after 10 for demo)")
        break

consumer.close()
"""