# Historical Weather Intelligence Data Pipeline and Dashboard for NY and SF (2021-2025)


## PROBLEM STATEMENT
Analyzing long-term climate patterns for major coastal metropolitan centers, New York and San Francisco ("NY" and "SF"), requires a robust and scalable data pipeline. This project focuses on gathering and processing 5 years of daily historical weather data for New York and San Francisco to enable comparative analysis of weather patterns and climate trends.


### DATA SOURCE 
https://open-meteo.com/


## TOOLS USED
| Component | Technology | Role in the Pipeline |
| :--- | :--- | :--- |
| **Orchestration** | **Kestra** | Automates batch processing, storage in data lake, transfer to warehouse, gold standard transformation of datasets  |
| **Cloud**	| **Google Cloud Services** |	Cloud platform and resource utilization for data lake and data warehouse |
| **IaC**	| **gcloud CLI / Terraform** |	Provisioning and managing cloud resources |
| **Batch Processing** | **Kestra python containers** | Fetches batches of data from API for NY and SF 5 years(2021-2025) |
| **Data Lake** | **Google Cloud Storage** | Acts as the landing zone for raw data --> scalable and durable |
| **Data Warehouse** | **BigQuery** | Clusters and Partitions the raw data and also perform large-scale historical queries. |
| **Transformation** | **dbt** | Models, Transforms and Cleans the raw API data into analytics-ready tables directly within the warehouse |
| **Visualization** | **Streamlit** | Delivers a final dashboard for side-by-side comparison of weather patterns between New York and San Francisco between 2021-2025 |
| **Environment** |	**uv**	 | Python package and dependencies management for local development and reproducibility |
