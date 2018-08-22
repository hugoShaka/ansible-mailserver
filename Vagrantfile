# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.vm.box = "debian/stretch64"
  config.vm.define "mailserver"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "test/test-vagrant.yml"
    ansible.sudo = true
    #ansible.verbose = 'vvv'
  end

  config.vm.provider "virtualbox" do |vb|
    config.vm.network "private_network", ip: "10.0.0.100"
  end
end

