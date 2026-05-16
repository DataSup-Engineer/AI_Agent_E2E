provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "bucket_name" {
  type = string
}

# GCS Bucket for Images
resource "google_storage_bucket" "image_bucket" {
  name          = var.bucket_name
  location      = "US"
  force_destroy = true
  
  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Cloud Run Service (Backend)
resource "google_cloud_run_service" "backend" {
  name     = "storygen-backend"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/storygen-backend"
        env {
          name  = "GOOGLE_CLOUD_PROJECT_ID"
          value = var.project_id
        }
        env {
          name  = "GENMEDIA_BUCKET"
          value = var.bucket_name
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow Unauthenticated Access (For demo purposes)
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.backend.name
  location = google_cloud_run_service.backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
