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
