# Provider configuration for Google Cloud Platform
provider "google" {
  project = var.project_id
  region  = var.region
}

# VPC network and subnets
resource "google_compute_network" "vpc_network" {
  name                    = "code-skeptic-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "code-skeptic-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

# Cloud Run services for microservices
resource "google_cloud_run_service" "api_service" {
  name     = "code-skeptic-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/code-skeptic-api:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service" "frontend_service" {
  name     = "code-skeptic-frontend"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/code-skeptic-frontend:latest"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud Functions for serverless components
resource "google_cloudfunctions_function" "code_analysis" {
  name        = "code-analysis-function"
  description = "Function to analyze code submissions"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_archive.name
  trigger_http          = true
  entry_point           = "analyze_code"
}

# Cloud Firestore database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# Cloud Storage buckets
resource "google_storage_bucket" "code_submissions" {
  name     = "${var.project_id}-code-submissions"
  location = var.region
}

resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function-bucket"
  location = var.region
}

resource "google_storage_bucket_object" "function_archive" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = "./function-source.zip"
}

# Cloud Pub/Sub topics and subscriptions
resource "google_pubsub_topic" "code_submission" {
  name = "code-submission-topic"
}

resource "google_pubsub_subscription" "code_analysis" {
  name  = "code-analysis-subscription"
  topic = google_pubsub_topic.code_submission.name

  ack_deadline_seconds = 20

  push_config {
    push_endpoint = google_cloudfunctions_function.code_analysis.https_trigger_url
  }
}

# Cloud API Gateway
resource "google_api_gateway_api" "api_gw" {
  provider = google-beta
  api_id   = "code-skeptic-api-gw"
}

resource "google_api_gateway_api_config" "api_gw" {
  provider      = google-beta
  api           = google_api_gateway_api.api_gw.api_id
  api_config_id = "code-skeptic-api-gw-config"

  openapi_documents {
    document {
      path     = "spec.yaml"
      contents = filebase64("${path.module}/api_spec.yaml")
    }
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "api_gw" {
  provider   = google-beta
  api_config = google_api_gateway_api_config.api_gw.id
  gateway_id = "code-skeptic-api-gw"
}

# Cloud Load Balancer
resource "google_compute_global_address" "default" {
  name = "code-skeptic-lb-ip"
}

resource "google_compute_global_forwarding_rule" "default" {
  name       = "code-skeptic-lb-forwarding-rule"
  target     = google_compute_target_http_proxy.default.id
  port_range = "80"
  ip_address = google_compute_global_address.default.address
}

resource "google_compute_target_http_proxy" "default" {
  name    = "code-skeptic-lb-proxy"
  url_map = google_compute_url_map.default.id
}

resource "google_compute_url_map" "default" {
  name            = "code-skeptic-lb-url-map"
  default_service = google_compute_backend_service.default.id
}

resource "google_compute_backend_service" "default" {
  name        = "code-skeptic-lb-backend"
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10

  backend {
    group = google_compute_instance_group.webservers.id
  }

  health_checks = [google_compute_health_check.default.id]
}

resource "google_compute_instance_group" "webservers" {
  name        = "code-skeptic-ig"
  description = "Code Skeptic instance group for load balancing"

  instances = [
    google_compute_instance.app_server.id,
  ]

  named_port {
    name = "http"
    port = "8080"
  }

  zone = "${var.region}-a"
}

resource "google_compute_health_check" "default" {
  name               = "code-skeptic-health-check"
  check_interval_sec = 5
  timeout_sec        = 5

  http_health_check {
    port = 8080
  }
}

# Cloud IAM roles and service accounts
resource "google_service_account" "code_skeptic_sa" {
  account_id   = "code-skeptic-sa"
  display_name = "Code Skeptic Service Account"
}

resource "google_project_iam_member" "code_skeptic_sa_roles" {
  for_each = toset([
    "roles/cloudfunctions.invoker",
    "roles/datastore.user",
    "roles/pubsub.publisher",
    "roles/storage.objectAdmin",
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.code_skeptic_sa.email}"
}

# HUMAN ASSISTANCE NEEDED
# The following resources need to be reviewed and potentially modified:
# 1. Ensure that the VPC network and subnet CIDR ranges are appropriate for your use case.
# 2. Review and adjust the Cloud Run service configurations, including memory limits and scaling options.
# 3. Verify that the Cloud Functions runtime and memory settings are suitable for your code analysis requirements.
# 4. Check if the Firestore database type (FIRESTORE_NATIVE) is the desired option for your project.
# 5. Review the Cloud Storage bucket names and ensure they are globally unique.
# 6. Adjust the Pub/Sub subscription ack_deadline_seconds if needed based on your code analysis function's execution time.
# 7. Review and modify the API Gateway configuration, including the API spec file path.
# 8. Verify that the Load Balancer configuration, including health checks and backend services, meets your requirements.
# 9. Review and potentially expand the IAM roles assigned to the service account based on your specific needs.