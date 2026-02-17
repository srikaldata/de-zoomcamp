{{ config(materialized='view') }}

with tripdata as 
(
  SELECT *
  FROM {{ source('staging', 'fhv_tripdata') }}
  -- Requirement: Filter out records where dispatching_base_num is null
  WHERE dispatching_base_num IS NOT NULL
)
select
    -- Identifiers
    dispatching_base_num,
    cast(pulocationid as integer) as pickup_location_id,
    cast(dolocationid as integer) as dropoff_location_id,
    
    -- Timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- Trip info
    sr_flag,
    affiliated_base_number
from tripdata

