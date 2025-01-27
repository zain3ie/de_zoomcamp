variable "credentials" {
  description = "credentials file location"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "project id"
  default     = "round-rain-449107-b2"
}

variable "region" {
  description = "region of the service"
  default     = "ASIA-SOUTHEAST2"
}

variable "bq_dataset_id" {
  description = "bigquery dataset name"
  default     = "terraform_dataset"
}

variable "storage_bucket_name" {
  description = "storage bucket name"
  default     = "terraform-bucket-449107-b2"
}
