
# UNCOMMENT AND UPDATE THE BELOW VARIABLE IF YOU WANT TO USE A SERVICE ACCOUNT KEY FILE INSTEAD OF APPLICATION DEFAULT CREDENTIALS
# variable "credentials" {
#   description = "My Credentials"
#   default     = "<Path to your Service Account json file>"
#   #ex: if you have a directory where this file is called keys with your service account json file
#   #saved there as my-creds.json you could use default = "./keys/my-creds.json"
# }

variable "project" {
  description = "Project ID"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_raw" {
  description = "Raw Data Dataset"
  default     = "weather_raw"
}

variable "bq_dataset_analytics" {
  description = "Analytics/dbt Dataset"
  default     = "weather_analytics"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}