# Project-specific variables
variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
}

variable "region" {
  description = "The region where resources will be created"
  type        = string
  default     = "us-central1"
}

# Environment-specific variables
variable "environment" {
  description = "The deployment environment (e.g., dev, staging, prod)"
  type        = string
}

variable "vpc_network_name" {
  description = "The name of the VPC network to use"
  type        = string
}

# Service configuration variables
variable "instance_type" {
  description = "The machine type for Compute Engine instances"
  type        = string
  default     = "n1-standard-1"
}

variable "min_replicas" {
  description = "Minimum number of instances in the autoscaling group"
  type        = number
  default     = 2
}

variable "max_replicas" {
  description = "Maximum number of instances in the autoscaling group"
  type        = number
  default     = 10
}

variable "target_cpu_utilization" {
  description = "Target CPU utilization for autoscaling"
  type        = number
  default     = 0.6
}

variable "db_instance_tier" {
  description = "The tier for the Cloud SQL instance"
  type        = string
  default     = "db-f1-micro"
}

# API keys and sensitive information
variable "github_token" {
  description = "GitHub personal access token for CI/CD"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Password for the database user"
  type        = string
  sensitive   = true
}

# HUMAN ASSISTANCE NEEDED
# The following variables may need to be adjusted or expanded based on specific project requirements:
# - Add any additional service-specific variables (e.g., for Cloud Storage, Cloud Functions, etc.)
# - Include variables for networking configuration if not using default settings
# - Consider adding variables for monitoring and logging configurations