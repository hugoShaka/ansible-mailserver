# -*- mode: ruby -*-
# vi: set ft=ruby :
#

Vagrant.configure(2) do |config|
  config.vm.box = "debian/buster64"

  config.vm.define "docker" do |subconfig|
    subconfig.vm.hostname = "docker-vm"
    subconfig.vm.provider "virtualbox" do |vb|
      vb.memory=4096
      vb.cpus=4
    end
    subconfig.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: ".git/"
  end
end
