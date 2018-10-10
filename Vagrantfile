# -*- mode: ruby -*-
# vi: set ft=ruby :
#

ansible_groups = {
  "dev:children" => ["dev-mail", "dev-test"],
  "dev-mail:children" => ["mta", "mda", "db" ],
  "dev-test" => ["tester"],
  "mta" => ["north", "south"],
  "mda" => ["north", "south"],
  "db" => ["north"],
}


Vagrant.configure(2) do |config|
  config.vm.box = "debian/stretch64"

  config.vm.define "north" do |subconfig|
    subconfig.vm.hostname = "mailserver-north"
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.100"
    end
  end
  config.vm.define "south" do |subconfig|
    subconfig.vm.hostname = "mailserver-south"
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.101"
    end
    subconfig.vm.provision "ansible" do |ansible|
      ansible.playbook = "test/mailserver-vagrant.yml"
      ansible.limit = "dev-mail"
      ansible.groups = ansible_groups
      ansible.become = true
    end
  end


  config.vm.define "tester" do |subconfig|
    subconfig.vm.hostname = "tester"
    subconfig.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "test/tester-vagrant.yml"
      ansible.become = true
      ansible.groups = ansible_groups
    end
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.50"
    end
  end
end

