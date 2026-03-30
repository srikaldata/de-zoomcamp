# Historical Weather Analytics Pipeline for NY and SF


## Problem statement:
Analyzing long-term climate patterns for major coastal urban centers requires a robust and scalable data architecture. This project focuses on gathering and processing 5 years of daily historical weather data for New York and San Francisco to enable comparative analysis of regional climate trends.


#### Data source:
https://open-meteo.com/

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
