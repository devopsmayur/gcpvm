# vm_creation.tf

provider "google" {
  project     = "hc-fff6e90888504253bd250e454a2"
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
resource "google_compute_instance" "mayur" {
  name         = "my-instance"
  machine_type = "n1-standard-1"
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
