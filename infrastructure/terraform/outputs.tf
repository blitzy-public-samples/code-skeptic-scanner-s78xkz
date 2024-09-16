# Output values for the infrastructure

# VPC network details
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.vpc.private_subnet_ids
}

# Service URLs and endpoints
output "frontend_url" {
  description = "URL of the frontend application"
  value       = module.frontend.url
}

output "backend_api_url" {
  description = "URL of the backend API"
  value       = module.backend.api_url
}

# Database connection strings
output "database_connection_string" {
  description = "Connection string for the main database"
  value       = module.database.connection_string
  sensitive   = true
}

output "redis_connection_string" {
  description = "Connection string for Redis cache"
  value       = module.redis.connection_string
  sensitive   = true
}

# Storage bucket names
output "static_assets_bucket" {
  description = "Name of the bucket for static assets"
  value       = module.storage.static_assets_bucket_name
}

output "user_uploads_bucket" {
  description = "Name of the bucket for user uploads"
  value       = module.storage.user_uploads_bucket_name
}

# API Gateway URL
output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = module.api_gateway.url
}

# Load Balancer IP address
output "load_balancer_ip" {
  description = "IP address of the load balancer"
  value       = module.load_balancer.ip_address
}

# HUMAN ASSISTANCE NEEDED
# The following outputs may need to be adjusted based on the actual module structure and naming conventions used in the project:
# - Verify that all module names (e.g., module.vpc, module.frontend, etc.) match the actual module names in the Terraform configuration.
# - Ensure that the output names within each module (e.g., vpc_id, connection_string, etc.) correspond to the actual output names defined in those modules.
# - Add any additional project-specific outputs that may be required.