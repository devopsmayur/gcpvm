# vm_creation.tf

provider "google" {
  project     = "hc-29a5d1b2591a4011824f3071b35"
  region      = "us-central1"
}

data "tfe_outputs" "test" {
    organization =  "devopsmayur"
    workspace = "gcpnw"
}

output "network_info" {
  value = data.tfe_outputs.google_compute_network.my_network
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

}
