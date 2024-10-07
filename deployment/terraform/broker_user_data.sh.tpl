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

# Use predefined IP addresses
BROKER1_IP="${broker1_private_ip}"
BROKER2_IP="${broker2_private_ip}"
BROKER3_IP="${broker3_private_ip}"
BROKER_ID="${broker_id}"

# Set LISTENER_IP based on BROKER_ID
if [ "$BROKER_ID" -eq 1 ]; then
    LISTENER_IP="$BROKER1_IP"
elif [ "$BROKER_ID" -eq 2 ]; then
    LISTENER_IP="$BROKER2_IP"
elif [ "$BROKER_ID" -eq 3 ]; then
    LISTENER_IP="$BROKER3_IP"
else
    LISTENER_IP="$BROKER3_IP"
fi

# Update docker-compose.yml for Broker 1 with dynamic IPs and node ID
sed -i "s/kafka1/$BROKER1_IP/g" /home/ubuntu/thesis/docker/broker.yaml
sed -i "s/kafka2/$BROKER2_IP/g" /home/ubuntu/thesis/docker/broker.yaml
sed -i "s/kafka3/$BROKER3_IP/g" /home/ubuntu/thesis/docker/broker.yaml
sed -i "s/local_listener/$LISTENER_IP/g" /home/ubuntu/thesis/docker/broker.yaml

sed -i 's/KAFKA_NODE_ID: 1/KAFKA_NODE_ID: ${broker_id}/' /home/ubuntu/thesis/docker/broker.yaml


# Run the service
sudo docker-compose -f /home/ubuntu/thesis/docker/broker.yaml up -d