#!/bin/bash

if [ ! -f /etc/apt/sources.list.d/ppa-configs.list ]; then
    cat > /etc/apt/sources.list.d/ppa-configs.list << 'EOF'
deb http://ppa.launchpad.net/0x2a/configs/ubuntu trusty main
EOF
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 87DED3F6
    apt-get -y update
    apt-get -y dist-upgrade
    apt-get -y install git librarian-puppet git puppet
    apt-get -y autoremove
    apt-get -y clean
fi

if [ ! -f /etc/puppet/Puppetfile ]; then
    cp /vagrant/puppet/Puppetfile /etc/puppet/Puppetfile
    pushd /etc/puppet
    librarian-puppet install
    popd
fi

diff -q /vagrant/puppet/Puppetfile /etc/puppet/Puppetfile &> /dev/null

if [ $? -ne 0 ]; then
    cp /vagrant/puppet/Puppetfile /etc/puppet/Puppetfile
    pushd /etc/puppet > /dev/null
    librarian-puppet update
    popd > /dev/null
fi
