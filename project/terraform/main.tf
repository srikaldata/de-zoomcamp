terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.25.0"
    }
  }
}

provider "google" {
  # Configuration options
  # UNCOMMENT THE BELOW VARIABLE AFTER UPDATING IN variables.tf IF YOU WANT TO USE A SERVICE ACCOUNT KEY FILE INSTEAD OF APPLICATION DEFAULT CREDENTIALS
  # credentials = file(var.credentials)
  project = var.project
  region  = var.region
}

# The Cloud Storage Bucket
resource "google_storage_bucket" "project-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# Dataset 1: For Raw Ingestion 
resource "google_bigquery_dataset" "weather_raw_dataset" {
  dataset_id = var.bq_dataset_raw
  location   = var.location
  delete_contents_on_destroy  = true
}

# Dataset 2: For dbt Transformations 
resource "google_bigquery_dataset" "weather_analytics_dataset" {
  dataset_id = var.bq_dataset_analytics
  location   = var.location
  delete_contents_on_destroy  = true
}