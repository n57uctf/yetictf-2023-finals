#!/bin/bash
source .env.student
vagrant validate
vagrant up --no-provision --provider virtualbox
vagrant provision
export UUID=$(cat .vagrant/machines/default/virtualbox/id)
export PKR_VAR_vagrantbox=$( vboxmanage showvminfo $UUID --machinereadable | grep -o -E 'vulnbox_default_[0-9]{1,}_[0-9]{1,}' | uniq)
export PKR_VAR_port=$(vboxmanage showvminfo $UUID --machinereadable | grep Forwarding  | awk -F',' '{print $4}')
vagrant halt
vagrant status
rm -rf output-vulnbox
packer init .
packer validate -var vagrantbox=$PKR_VAR_vagrantbox -var port=$PKR_VAR_port -var username=$PKR_VAR_username -var password=$PKR_VAR_password -var event=$PKR_VAR_event -var services=$PKR_VAR_services  .
packer build -var vagrantbox=$PKR_VAR_vagrantbox -var port=$PKR_VAR_port -var username=$PKR_VAR_username -var password=$PKR_VAR_password -var event=$PKR_VAR_event -var services=$PKR_VAR_services .