# Historical Weather Analytics Pipeline for NY and SF


## Problem statement:
Analyzing long-term climate patterns for major coastal urban centers requires a robust and scalable data architecture. This project focuses on gathering and processing 5 years of daily historical weather data for New York and San Francisco to enable comparative analysis of regional climate trends.


#### Data source:
https://open-meteo.com/

#### Tools used:
| Component | Technology | Role in the Pipeline |
| :--- | :--- | :--- |
| **Orchestration** | **Kestra** | Automates the 10-batch ingestion process (2 cities x 5 years) with built-in error handling and retries. |
| **Data Lake** | **Google Cloud Storage** | Acts as the landing zone for raw JSON and CSV data, ensuring a scalable and durable foundation. |
| **Data Warehouse** | **BigQuery** | Provides the compute power to handle large-scale historical queries. |
| **Transformation** | **dbt** | Models and cleans the raw API data into analytics-ready tables directly within the warehouse. |
| **Visualization** | **Streamlit** | Delivers a final dashboard for side-by-side comparison of weather patterns between New York and San Francisco. |

## google cloud platform
* use a service account, generate key and use it for terraform
* or login as follows using the cli and ui in browser:
`gcloud auth application-default login`

* make sure to logout once completed using the folowign two commands
`gcloud auth application-default revoke`
`gcloud auth revoke`

## terraform
* created main.tf and variables.tf
* `terraform fmt` to prettify the .tf files
* `terraform plan` to validate the config
* `terraform apply` to apply the config in the GCP
* make sure to run `terraform destroy` upon completion
