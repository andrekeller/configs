# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "puppetlabs/ubuntu-14.04-64-nocm"
  config.vm.hostname = "configs.vagrant"

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = false
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.ssh.forward_agent = true

  config.vm.provider "virtualbox" do |vb|
      vb.name = "configs"
      vb.memory = 1024
      vb.cpus = 2
  end

  config.vm.network "forwarded_port", guest: 1443, host: 1443

  config.vm.provision "shell", path: "puppet/provision.sh"
  config.vm.provision "puppet" do |puppet|
      puppet.facter = {
          "vagrant" => "1"
      }
      puppet.manifests_path = ["vm", "/vagrant/puppet/manifests"]
      puppet.hiera_config_path = "puppet/hiera.yaml"
  end
end
