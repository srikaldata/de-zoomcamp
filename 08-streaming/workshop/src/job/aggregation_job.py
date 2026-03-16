import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

def create_events_source_kafka(t_env):
    table_name = "green_trips"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            vendor_id INT,
            lpep_pickup_datetime STRING,
            lpep_dropoff_datetime STRING,
            PULocationID INT,
            DOLocationID INT,
            passenger_count DOUBLE, -- Changed from INT to DOUBLE to handle NaN
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-homework-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true', -- Skips the record if JSON is totally broken
            'json.fail-on-missing-field' = 'false'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_sink_postgres(t_env, table_name, schema_ddl):
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            {schema_ddl}
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

def run_job(question_number):
    # 1. Setup Environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # 2. Define Source
    source = create_events_source_kafka(t_env)

    if question_number == 4:
        # QUESTION 4: 5-Min Tumbling Window
        sink_q4 = create_sink_postgres(t_env, 'q4_results',
                    "window_start TIMESTAMP(3), PULocationID INT, num_trips BIGINT")

        t_env.execute_sql(f"""
            INSERT INTO {sink_q4}
            SELECT window_start, PULocationID, COUNT(*) as num_trips
            FROM TABLE(TUMBLE(TABLE {source}, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTE))
            GROUP BY window_start, window_end, PULocationID
        """).wait()

    elif question_number == 5:
        # QUESTION 5: 5-Min Session Window
        sink_q5 = create_sink_postgres(t_env, 'q5_results',
                    """
                    window_start TIMESTAMP(3),
                    window_end TIMESTAMP(3),
                    PULocationID INT,
                    num_trips BIGINT,
                    PRIMARY KEY (window_start, PULocationID) NOT ENFORCED
                    """)

        t_env.execute_sql(f"""
            INSERT INTO {sink_q5}
            SELECT window_start, window_end, PULocationID, COUNT(*) as num_trips
            FROM TABLE(SESSION(TABLE {source}, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTE))
            GROUP BY window_start, window_end, PULocationID
        """).wait()

    elif question_number == 6:
        # QUESTION 6: 1-Hour Tumbling Window
        sink_q6 = create_sink_postgres(t_env, 'q6_results',
                    """
                    window_start TIMESTAMP(3),
                    total_tip DOUBLE,
                    PRIMARY KEY (window_start) NOT ENFORCED
                    """)

        t_env.execute_sql(f"""
            INSERT INTO {sink_q6}
            SELECT window_start, SUM(tip_amount) as total_tip
            FROM TABLE(TUMBLE(TABLE {source}, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR))
            GROUP BY window_start, window_end
        """) # Removed .wait()

if __name__ == '__main__':
    # Change the number below to 4, 5, or 6 to run the specific homework task
    run_job(question_number=5)