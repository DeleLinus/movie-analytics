resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.wizeline_capstone_bucket.name
  role = "roles/storage.admin"
  member = "allUsers"
}


resource "google_storage_bucket" "wizeline_capstone_bucket" {
  name          = var.bucket_name
  location      = var.location
  storage_class = var.storage_class
  force_destroy = true
  labels = {
    environment = var.environment 
  }
}