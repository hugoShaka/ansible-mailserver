# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.vm.box = "debian/stretch64"
  config.vm.define "mailserver" do |subconfig|
    subconfig.vm.provision "ansible" do |ansible|
      ansible.playbook = "test/mailserver-vagrant.yml"
      ansible.become = true
    end
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.100"
    end
  end
  config.vm.define "tester" do |subconfig|
    subconfig.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "test/tester-vagrant.yml"
      ansible.become = true
    end
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.50"
    end
  end
end

