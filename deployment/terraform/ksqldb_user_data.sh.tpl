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
git clone https://github.com/iqbalhanif313/shm-blueprint.git
cd shm-blueprint

# Use predefined IP addresses
BROKER1_IP="${broker1_private_ip}"
BROKER2_IP="${broker2_private_ip}"
BROKER3_IP="${broker3_private_ip}"
SCHEMA_REGISTRY_IP="${schema_registry_private_ip}"
CONNECT_PRIVATE_IP="${connect_private_ip}"
HOST_NAME="${ksqldb_host_name}"


# Update docker-compose.yml for Broker 1 with dynamic IPs and node ID
sed -i "s/kafka1/$BROKER1_IP/g" /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml
sed -i "s/kafka2/$BROKER2_IP/g" /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml
sed -i "s/kafka3/$BROKER3_IP/g" /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml
sed -i "s/schema-registry/$SCHEMA_REGISTRY_IP/g" /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml
sed -i "s/connect/$CONNECT_PRIVATE_IP/g" /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml
sed -i "s/host-name/$HOST_NAME/g" /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml

# Run the service
sudo docker-compose -f /home/ubuntu/shm-blueprint/deployment/docker/ksqldb.yaml up -d