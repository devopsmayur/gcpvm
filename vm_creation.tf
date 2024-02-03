# vm_creation.tf

provider "google" {
  credentials = file("<path-to-your-service-account-key.json>")
  project     = "your-gcp-project-id"
  region      = "us-central1"
}

# Input variables to receive network information from Workspace 1
variable "network_info" {
  description = "Network information from Workspace 1"
}

# Create a virtual machine instance
resource "google_compute_instance" "my_instance" {
  name         = "my-instance"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = var.network_info.self_link
  }
}
