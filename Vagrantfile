# -*- mode: ruby -*-
# vi: set ft=ruby :
#

ansible_groups = {
  "dev:children" => ["dev-mail", "dev-test"],
  "dev-mail:children" => ["mail"],
  "dev-test:children" => ["test"],
  "mail:children" => ["mta", "mda", "db" ],
  "test" => ["tester"],
  "mta" => ["north", "south"],
  "mda" => ["north", "south"],
  "db" => ["north"],
}

ansible_host_vars = {
  "north" => {"ispmail_dovecot_replication_peer" => "south.mail.local"},
  "south" => {"ispmail_dovecot_replication_peer" => "north.mail.local"}
}


Vagrant.configure(2) do |config|
  config.vm.box = "debian/stretch64"

  config.vm.define "north" do |subconfig|
    subconfig.vm.hostname = "north.mail.local"
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.100"
    end
  end
  config.vm.define "south" do |subconfig|
    subconfig.vm.hostname = "south.mail.local"
    subconfig.vm.provider "virtualbox" do |vb|
      subconfig.vm.network "private_network", ip: "10.0.0.101"
    end
    subconfig.vm.provision "ansible" do |ansible|
      ansible.playbook = "test/mailserver-vagrant.yml"
      ansible.limit = "mail"
      ansible.groups = ansible_groups
      ansible.host_vars = ansible_host_vars
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
