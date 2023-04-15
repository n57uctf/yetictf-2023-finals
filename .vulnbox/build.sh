#!/bin/bash
export $(grep -v '^#' .env | xargs -d '\n')
export $(grep -v '^#' .env.student | xargs -d '\n')
vagrant validate
vagrant up --provision --provider virtualbox
export UUID=$(cat .vagrant/machines/default/virtualbox/id)
export PKR_VAR_vagrantbox=$( vboxmanage showvminfo $UUID --machinereadable | grep -o -E 'vulnbox_default_[0-9]{1,}_[0-9]{1,}' | uniq)
export PKR_VAR_port=$(vboxmanage showvminfo $UUID --machinereadable | grep Forwarding  | awk -F',' '{print $4}')
vagrant halt
vagrant status
rm -rf output-vulnbox
packer init .
packer validate .
packer build .