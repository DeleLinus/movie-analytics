variable "project_id" {
  type          = string
  description   = "The Project ID in which will be deployed the services"
}
variable "region" {
  description = "Region where the instance will live"
}
variable "zone" {
  type          = string
  description   = "The zone in which the GCP bucket will be created."
}

variable "location" {
  description = "The preferred compute engine"
}

variable "instance_name" {
  description = "Name for the sql instance database"
  default     = "data-bootcamp-capstone"
}

variable "database_version" {
  description = "The MySQL, PostgreSQL or SQL Server (beta) version to use. "
  default     = "POSTGRES_12"
}

variable "instance_tier" {
  description = "Sql instance tier"
  default     = "db-f1-micro"
}

variable "disk_space" {
  description = "Size of the disk in the sql instance"
  default     = 10
}

variable "database_name" {
  description = "Name for the database to be created"
  default     = "dbname"
}

variable "db_username" {
  description = "Username credentials for root user"
  default     = "dbuser"
}
variable "db_password" {
  description = "Password credentials for root user"
  default     = "dbpassword"
}

