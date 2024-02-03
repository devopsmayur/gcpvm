# vm_creation.tf

provider "google" {
  project     = "hc-29a5d1b2591a4011824f3071b35"
  region      = "us-central1"
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

