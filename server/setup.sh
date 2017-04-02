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

# General utilities
apt install vim tree git htop ssh python-virtualenv

# Open ports for SSH and HTTP
ufw enable
ufw allow 22
ufw allow 8000
ufw reload

# Set SSH to only allow auth via keys
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config
service ssh restart

# Setup django project
git clone https://github.com/ObiJuanKenobi/Prison-Garden-Application.git
# cd Prison-Garden-Application
# virtualenv venv
# . venv/bin/activate
# pip install django mysql-python
# deactivate

# Run the django project
#
# cd Prison-Garden-Application
# git pull
# . venv/bin/activate
# python manage.py runserver
# <Ctrl-c to stop>
# deactivate

echo 'Please restart in order to complete the changes.'
