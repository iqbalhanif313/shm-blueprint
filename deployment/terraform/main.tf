# Specify the provider and region
provider "aws" {
  region = "ap-southeast-2"  # Change to your desired region
}

# Create a VPC
resource "aws_vpc" "kafka_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "kafka-vpc"
  }
}

# Create subnets across three different availability zones
resource "aws_subnet" "kafka_subnet_az1" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-southeast-2a"  # Change based on your region's AZs
  tags = {
    Name = "kafka-subnet-az1"
  }
}

resource "aws_subnet" "kafka_subnet_az2" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-southeast-2b"  # Change based on your region's AZs
  tags = {
    Name = "kafka-subnet-az2"
  }
}

resource "aws_subnet" "kafka_subnet_az3" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "kafka-subnet-az3"
  }
}

resource "aws_subnet" "control_center_subnet" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "control-center-subnet"
  }
}


resource "aws_subnet" "schema_registry_subnet" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.5.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "schema-registry-subnet"
  }
}

resource "aws_subnet" "connect_subnet" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.6.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "connect-subnet"
  }
}

resource "aws_subnet" "ksqldb_subnet" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.7.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "ksqldb-subnet"
  }
}

resource "aws_subnet" "ksqldb2_subnet" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.8.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "ksqldb2-subnet"
  }
}

resource "aws_subnet" "influxdb_subnet" {
  vpc_id     = aws_vpc.kafka_vpc.id
  cidr_block = "10.0.9.0/24"
  availability_zone = "ap-southeast-2c"  # Change based on your region's AZs
  tags = {
    Name = "ksqldb2-subnet"
  }
}

# Create an Internet Gateway for public subnets
resource "aws_internet_gateway" "kafka_igw" {
  vpc_id = aws_vpc.kafka_vpc.id
  tags = {
    Name = "kafka-igw"
  }
}

# Create route table for the VPC
resource "aws_route_table" "kafka_route_table" {
  vpc_id = aws_vpc.kafka_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.kafka_igw.id
  }
}

# Associate route table with subnets
resource "aws_route_table_association" "kafka_rta_az1" {
  subnet_id      = aws_subnet.kafka_subnet_az1.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "kafka_rta_az2" {
  subnet_id      = aws_subnet.kafka_subnet_az2.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "kafka_rta_az3" {
  subnet_id      = aws_subnet.kafka_subnet_az3.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "control_center_rta" {
  subnet_id      = aws_subnet.control_center_subnet.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "schema_registry_rta" {
  subnet_id      = aws_subnet.schema_registry_subnet.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "connect_rta" {
  subnet_id      = aws_subnet.connect_subnet.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "ksqldb_rta" {
  subnet_id      = aws_subnet.ksqldb_subnet.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "ksqldb2_rta" {
  subnet_id      = aws_subnet.ksqldb2_subnet.id
  route_table_id = aws_route_table.kafka_route_table.id
}

resource "aws_route_table_association" "influxdb_rta" {
  subnet_id      = aws_subnet.influxdb_subnet.id
  route_table_id = aws_route_table.kafka_route_table.id
}


# Create Security Group for Kafka brokers
resource "aws_security_group" "kafka_sg" {
  vpc_id = aws_vpc.kafka_vpc.id

  # Allow SSH access from any IP (modify as needed for security)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Or restrict to a specific IP range
  }

  # Allow ICMP (ping) within the VPC
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["10.0.0.0/16"]  # Allow ICMP within the VPC
  }

  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Adjust for your specific access needs
  }
  ingress {
    from_port   = 9021
    to_port     = 9021
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Adjust for your specific access needs
  }

  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Adjust for your specific access needs
  }

  ingress {
    from_port   = 8083
    to_port     = 8083
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Adjust for your specific access needs
  }

  ingress {
    from_port   = 8088
    to_port     = 8088
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Adjust for your specific access needs
  }

  ingress {
    from_port   = 8086
    to_port     = 8086
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Adjust for your specific access needs
  }


  ingress {
    from_port   = 8888
    to_port     = 8888
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Adjust for your specific access needs
  }

  ingress {
    from_port   = 29092
    to_port     = 29092
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Adjust for your specific access needs
  }

  ingress {
    from_port   = 29093
    to_port     = 29093
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Adjust for your specific access needs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "kafka-sg"
  }
}

# EC2 Instances for Kafka Brokers

# Broker 1 (Publicly exposed)
resource "aws_instance" "kafka_broker_1" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.kafka_subnet_az1.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "kafka-broker-1"
  }
  private_ip                  = var.broker1_private_ip

  user_data = templatefile("broker_user_data.sh.tpl", {
    broker_id           = 1
    broker1_private_ip  = var.broker1_private_ip
    broker2_private_ip  = var.broker2_private_ip
    broker3_private_ip  = var.broker3_private_ip
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits (typically 30 GB)
    volume_type = "gp3"
  }
}
#
# Broker 2 (Internal)
resource "aws_instance" "kafka_broker_2" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.kafka_subnet_az2.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "kafka-broker-2"
  }
  private_ip                  = var.broker2_private_ip

  user_data = templatefile("broker_user_data.sh.tpl", {
    broker_id           = 2
    broker1_private_ip  = var.broker1_private_ip
    broker2_private_ip  = var.broker2_private_ip
    broker3_private_ip  = var.broker3_private_ip
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}

# Broker 3 (Internal)
resource "aws_instance" "kafka_broker_3" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.kafka_subnet_az3.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "kafka-broker-3"
  }
  private_ip                  = var.broker3_private_ip
  user_data = templatefile("broker_user_data.sh.tpl", {
    broker_id           = 3
    broker1_private_ip  = var.broker1_private_ip
    broker2_private_ip  = var.broker2_private_ip
    broker3_private_ip  = var.broker3_private_ip
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}


resource "aws_instance" "schema_registry" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.micro"     # Free-tier eligible instance
  subnet_id       = aws_subnet.schema_registry_subnet.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "schema_registry"
  }
  private_ip                  = var.schema_registry_private_ip
  user_data = templatefile("schema_registry_user_data.sh.tpl", {
    broker1_private_ip  = aws_instance.kafka_broker_1.private_ip
    broker2_private_ip  = aws_instance.kafka_broker_2.private_ip
    broker3_private_ip  = aws_instance.kafka_broker_3.private_ip
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}


resource "aws_instance" "connect" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.connect_subnet.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "connect"
  }
  private_ip                  = var.connect_private_ip
  user_data = templatefile("connect_user_data.sh.tpl", {
    broker1_private_ip  = aws_instance.kafka_broker_1.private_ip
    broker2_private_ip  = aws_instance.kafka_broker_2.private_ip
    broker3_private_ip  = aws_instance.kafka_broker_3.private_ip
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}


resource "aws_instance" "ksqldb" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.ksqldb_subnet.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "ksqldb"
  }
  private_ip                  = var.ksqldb_private_ip
  user_data = templatefile("ksqldb_user_data.sh.tpl", {
    broker1_private_ip  = aws_instance.kafka_broker_1.private_ip
    broker2_private_ip  = aws_instance.kafka_broker_2.private_ip
    broker3_private_ip  = aws_instance.kafka_broker_3.private_ip
    connect_private_ip = aws_instance.connect.private_ip
    schema_registry_private_ip = aws_instance.schema_registry.private_ip
    ksqldb_host_name = "ksqldb-server"
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}

resource "aws_instance" "ksqldb2" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.ksqldb2_subnet.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "ksqldb2"
  }
  private_ip       = var.ksqldb2_private_ip
  user_data = templatefile("ksqldb_user_data.sh.tpl", {
    broker1_private_ip  = aws_instance.kafka_broker_1.private_ip
    broker2_private_ip  = aws_instance.kafka_broker_2.private_ip
    broker3_private_ip  = aws_instance.kafka_broker_3.private_ip
    connect_private_ip = aws_instance.connect.private_ip
    schema_registry_private_ip = aws_instance.schema_registry.private_ip
    ksqldb_host_name = "ksqldb2-server"
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}

resource "aws_instance" "influxdb" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.micro"     # Free-tier eligible instance
  subnet_id       = aws_subnet.influxdb_subnet.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "influxdb"
  }
  private_ip       = var.influxdb_private_ip
  user_data = templatefile("influxdb_user_data.sh.tpl", {})

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}

resource "aws_instance" "control_center" {
  ami             = "ami-0892a9c01908fafd1" # Use a valid AMI ID for ap-southeast-1 (adjust based on your requirement)
  instance_type   = "t2.large"     # Free-tier eligible instance
  subnet_id       = aws_subnet.control_center_subnet.id
  key_name        = "thesis-kafka"
  vpc_security_group_ids = [aws_security_group.kafka_sg.id]
  associate_public_ip_address = true
  tags = {
    Name = "control-center"
  }
  private_ip                  = var.control_center_private_ip
  user_data = templatefile("control_center_user_data.sh.tpl", {
    broker1_private_ip  = aws_instance.kafka_broker_1.private_ip
    broker2_private_ip  = aws_instance.kafka_broker_2.private_ip
    broker3_private_ip  = aws_instance.kafka_broker_3.private_ip
    schema_registry_private_ip = aws_instance.schema_registry.private_ip
    connect_private_ip = aws_instance.connect.private_ip
    ksqldb_private_ip = aws_instance.ksqldb.private_ip
    ksqldb2_private_ip = aws_instance.ksqldb2.private_ip
  })

  root_block_device {
    volume_size = 30 # Ensure this is within the free-tier limits
    volume_type = "gp3"
  }
}

# Output the public IP of the exposed broker
output "kafka_broker_ips" {
  value = [
    aws_instance.kafka_broker_1.public_ip,
    aws_instance.kafka_broker_2.public_ip,
    aws_instance.kafka_broker_3.public_ip,
    aws_instance.control_center.public_ip
  ]
}
