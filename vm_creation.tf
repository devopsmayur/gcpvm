# vm_creation.tf

provider "google" {
  project     = "hc-9f9cfc28ffd7455db4a08ac7a0e"
  region      = "us-central1"
}

data "tfe_outputs" "test" {
    organization =  "devopsmayur"
    workspace = "gcpnw"
}

output "network_info" {
  value = data.tfe_outputs.test.id
}


# Create a virtual machine instance
resource "google_compute_instance" "world1" {
  name         = "my-instance7"
  machine_type = "t3.medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

}
