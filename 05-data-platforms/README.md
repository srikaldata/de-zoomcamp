# QUESTION 1 - Pipeline Structure
* Bruin Pipeline Structure in a Bruin project, what are the required files/directories? 
```
└── your-project-name/
    ├── .bruin.yml
    └── pipeline/
        ├── pipeline.yml
        └── assets/
            ├── ___sql
            └── _____.py
```
* ANSWER: 
    * .bruin.yml 
    * pipeline/ 
        * pipeline.yml
        * assets/


# QUESTION 2 - Materialization Strategies
* Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?
* ANSWER: 
    * `time_interval`
    * because it refreshes the records within the time window defined


# QUESTION 3 - Pipeline Variables:
* Running the pipeline to only process yellow taxis
* ANSWER:
    * `bruin run --var 'taxi_types=["yellow"]'`
    * the `--var` flag is used to override existing values


# QUESTION 4 - Running with Dependencies:
* run ingestion/trips.py asset and plus all downstream assets
* ANSWER:
    * `bruin run ingestion/trips.py --downstream`
    * `--downstream` flag makes sure all the downstream dependencies are run after executing the current asset which is run


# QUESTION 5 - Quality Checks:
* pickup_datetime column in your trips table never has NULL values
* ANSWER:
    * `name: not_null`
    * not_null makes sure no null values are present in a column
    * if null values are present in the specified column, the quality check fails and the execution stops

