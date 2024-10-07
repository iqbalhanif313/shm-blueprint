#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y docker.io git curl
sudo systemctl start docker
sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

cd /home/ubuntu
git clone https://github.com/iqbalhanif313/thesis.git
cd thesis


# Run the service
sudo docker-compose -f /home/ubuntu/thesis/docker/influxdb.yaml up -d