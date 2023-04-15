packer {
  required_plugins {
    virtualbox = {
      version = ">= 0.0.1"
      source  = "github.com/hashicorp/virtualbox"
    }
  }
}

variable "bridgeadapter" { 
  type = string
  default = "eth0" 
}

variable "username" {
  type = string
}

variable "password" {
  type = string
}

variable "event" {
  type = string
}

variable "vagrantbox" {
  type = string
}

variable "port" {
  type = number
}

variable "services" {
  type = list(string)
}

source "virtualbox-vm" "vulnbox" {
  vm_name = var.vagrantbox
  headless = true
  ssh_username = "vagrant"
  ssh_private_key_file = "./.vagrant/machines/default/virtualbox/private_key"
  keep_registered = false
  shutdown_command = "sudo shutdown -P now"
  guest_additions_mode = "disable"
  skip_nat_mapping = true
  ssh_port = var.port
  vboxmanage_post = [
    ["modifyvm", "{{.Name}}", "--nic2", "bridged"],
    ["modifyvm", "{{.Name}}", "--bridgeadapter2", var.bridgeadapter],
    ["modifyvm", "{{.Name}}", "--macaddress2", "0274616e756b"],
    ["modifyvm", "{{.Name}}", "--cableconnected1", "off"],
    ["sharedfolder", "remove", "{{.Name}}", "--name", "vagrant"]
  ]
  export_opts = [
    "--manifest",
    "--vsys", "0",
    "--vmname", "${var.event}",
    "--description", "ssh ${var.username}@192.168.<N>.2\nPassword: ${var.password}\nПримечание:\n- Bridge-адаптер - второй из четырех\n"
  ]
  output_filename = "${var.event}"
  format = "ova"
}

build {
  sources = [
    "source.virtualbox-vm.vulnbox",
  ]

  provisioner "shell" {
    environment_vars = [
      "PWD=/vagrant"
    ]
    inline = [
      "sudo -E useradd -d /home/${var.username} -m -G docker,wheel ${var.username}",
      "echo '${var.username}:${var.password}' | sudo -E chpasswd"
    ]
  }

  provisioner "shell" {
    environment_vars = [
      "PWD=/vagrant",
      "HOME=/home/${var.username}"
    ]
    inline = [
      for s in var.services: "sudo cp -r /vagrant/${s}/${s} /home/${var.username}/${s}"
    ]
  }
  provisioner "shell" {
    environment_vars = [
      "PWD=/vagrant",
      "HOME=/home/${var.username}"
    ]
    inline = [
      "cd /vagrant",
      "sudo -E -u ${var.username} rm -rf /home/${var.username}/.jury",
      "sudo -E -u ${var.username} find /home/${var.username}/ -name \"host_prepare.sh\" -exec echo FOUND PREPARE {} \\; -exec bash {} \\;",
      "sudo -E -u ${var.username} find /home/${var.username}/ -name \"docker-compose.yml\" -exec echo FOUND docker-compose {} \\; -exec docker-compose -f {} up --build -d \\;",
      "sudo -E -u ${var.username} find /home/${var.username}/ -name \"docker-compose.yml\" -exec docker-compose -f {} down \\;"
    ]
  }
  
  provisioner "shell" {
    environment_vars = [
      "PWD=/vagrant",
      "HOME=/home/${var.username}"
    ]
    inline = [
      "cd /vagrant",
      "sudo -E -u ${var.username} rm -rf /home/${var.username}/vulnogramm/Exsample",
      # TODO: Fix deletion of BankService
      "sudo -E -u ${var.username} rm -rf /home/${var.username}/BankService/backend",
      "echo -e 'y\\ny' | sudo -E docker image prune -a",
      "echo -e 'y\\ny' | sudo -E docker container prune"
    ]
  }

  provisioner "shell"{
    environment_vars = [
      "PWD=/vagrant"
    ]
    inline = [
      "history -c",
      "sudo -E cp /etc/systemd/network/eth0.network /etc/systemd/network/eth1.network",
      "sudo -E sed -i 's/eth0/eth1/' /etc/systemd/network/eth1.network",
      "sudo -E usermod -L vagrant"
    ]
  }
}
