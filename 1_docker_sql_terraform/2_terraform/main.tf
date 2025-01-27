terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = var.credentials
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "terraform-bucket" {
  name          = var.storage_bucket_name
  location      = var.region
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

resource "google_bigquery_dataset" "terraform-dataset" {
  dataset_id = var.bq_dataset_id
  location   = var.region
}
