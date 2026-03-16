from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

def run_q6():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Source: Green Trips Kafka
    t_env.execute_sql("""
        CREATE TABLE source (
            tip_amount DOUBLE,
            lpep_pickup_datetime STRING,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true'
        )
    """)

    # Sink: Postgres Table 'q6'
    t_env.execute_sql("""
        CREATE TABLE sink (
            window_start TIMESTAMP(3),
            total_tip DOUBLE,
            PRIMARY KEY (window_start) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'q6',
            'username' = 'postgres',
            'password' = 'postgres'
        )
    """)

    # logic: 1-hour Tumble Window
    t_env.execute_sql("""
        INSERT INTO sink
        SELECT window_start, SUM(tip_amount) as total_tip
        FROM TABLE(
            TUMBLE(TABLE source, DESCRIPTOR(event_timestamp), INTERVAL '1' HOURS)
        )
        GROUP BY window_start, window_end
    """).wait()

if __name__ == '__main__':
    run_q6()