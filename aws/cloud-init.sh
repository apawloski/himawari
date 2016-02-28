#! /bin/bash

# This runs on an ec2 instance
# It runs himawari.py and terminates the instance upon completion
#
# This script is ubuntu-specific

apt-get update
apt-get install -y git python-dev python-pip libjpeg-dev zlib1g-dev libfreetype6-dev

git clone https://github.com/apawloski/himawari.git
cd himawari
pip install -r requirements.txt
python himawari.py

shutdown -h now
