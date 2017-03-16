#!/bin/bash

#
# Script for setting up a new Ubuntu 16.04 server.
# Must be run as root.
#

# Ensure root user
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# General updates
apt update
apt upgrade

# General utities
apt install vim tree git htop ssh

# Django-specific utilities
apt install django

# Open ports for SSH and HTTPS
ufw enable
ufw allow 22
ufw allow 443
ufw reload

# Set SSH to only allow auth via keys
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config
service ssh restart

echo 'Please restart in order to complete the changes.'
