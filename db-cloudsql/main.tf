resource "google_sql_database_instance" "sql_instance" {
  name              = var.instance_name
  database_version  = var.database_version
  region            = var.region

  settings {
    tier      = var.instance_tier
    edition   = "ENTERPRISE"
    disk_size = var.disk_space
    

    location_preference {
      zone = var.zone
    }

    ip_configuration {
      authorized_networks {
        value           = "0.0.0.0/0"
        name            = "test-cluster"
      }
    }
  }

  deletion_protection = "false"
}

resource "google_sql_database" "database" {
  name     = var.database_name
  instance = google_sql_database_instance.sql_instance.name
}

resource "google_sql_user" "users" {
  name     = var.db_username
  instance = google_sql_database_instance.sql_instance.name
  # host     = "*" # should not be set for postgres sql (https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_user)
  password = var.db_password
}