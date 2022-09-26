resource "aws_vpc" "vpc" {
    cidr_block           = var.cidr-block-vpc
    enable_dns_hostnames = true
    enable_dns_support   = true

    tags = {
        Name = "${var.project-name}-VPC"
  }
}

resource "aws_subnet" "private-subnet-a" {
    vpc_id            = aws_vpc.vpc.id
    cidr_block        = var.cidr-block-subnet[0]
    availability_zone = var.availability-zone[0]

    tags = {
        Name = "${var.project-name}-Private-Subnet-A"
  }
}

resource "aws_subnet" "private-subnet-b" {
    vpc_id            = aws_vpc.vpc.id
    cidr_block        = var.cidr-block-subnet[1]
    availability_zone = var.availability-zone[1]

    tags = {
        Name = "${var.project-name}-Private-Subnet-B"
  }
}

resource "aws_ec2_transit_gateway" "transit-gateway" {
    description                     = "${var.project-name}-TGW"
    amazon_side_asn                 = 64512
    default_route_table_association = "enable"
    dns_support                     = "enable"
    vpn_ecmp_support                = "enable"

    tags = {
        Name = "${var.project-name}-TGW"                 
    }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "transit-gateway-attachment" {
    subnet_ids         = [aws_subnet.private-subnet-a.id, aws_subnet.private-subnet-b.id]
    transit_gateway_id = aws_ec2_transit_gateway.transit-gateway.id
    vpc_id             = aws_vpc.vpc.id

    tags = {
        Name = "${var.project-name}-Attachment"
  }
}

resource "aws_route_table" "private-rt" {
    vpc_id = aws_vpc.vpc.id

    tags = {
        Name = "${var.project-name}-Route-table"
  }  
}

resource "aws_route" "transit-gateway-route" {
    route_table_id         = aws_route_table.private-rt.id
    transit_gateway_id     = aws_ec2_transit_gateway.transit-gateway.id
    destination_cidr_block = "0.0.0.0/0"     
}

resource "aws_route_table_association" "private-subnet-a" {
    subnet_id      = aws_subnet.private-subnet-a.id
    route_table_id = aws_route_table.private-rt.id
}

resource "aws_route_table_association" "private-subnet-b" {
    subnet_id      = aws_subnet.private-subnet-a.id
    route_table_id = aws_route_table.private-rt.id
}

resource "aws_security_group" "linux-security-group" {
    vpc_id      = aws_vpc.vpc.id
    name        = "${var.project-name}-Linux-SG"
    description = "Security group for linux instances"   

    ingress {
    description = "Allow SSH IPv4 IN from Azure"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.azure-cidr-block]
  }
    ingress {
    description = "Allow ICMP IPv4 IN from Azure"
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = [var.azure-cidr-block]
  }
    tags = {
        Name = "${var.project-name}-Linux-SG"
  }      
}

resource "aws_security_group" "windows-security-group" {
    vpc_id      = aws_vpc.vpc.id
    name        = "${var.project-name}-Windows-SG"
    description = "Security group for windows instances"

    ingress {
    description = "Allow RDP IPv4 IN from Azure"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = [var.azure-cidr-block]
  }
    ingress {
    description = "Allow ICMP IPv4 In from Azure"
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = [var.azure-cidr-block]
  }

    tags = {
        Name = "${var.project-name}-Windows-SG"
  }       
}

resource "aws_security_group_rule" "security-group-linux-selfreference-rule" {
    type                     = "ingress"
    protocol                 = -1
    from_port                = 0
    to_port                  = 0
    security_group_id        = aws_security_group.linux-security-group.id
    source_security_group_id = aws_security_group.linux-security-group.id
    description              = "Linux SG Self Reference"  
}

resource "aws_security_group_rule" "security-group-windows-selfreference-rule" {
    type                     = "ingress"
    protocol                 = -1
    from_port                = 0
    to_port                  = 0
    security_group_id        = aws_security_group.windows-security-group.id
    source_security_group_id = aws_security_group.windows-security-group.id
    description              = "Windows SG Self Reference"
}

resource "aws_vpc_endpoint" "ssm-interfave-endpoint" {
    service_name        = "com.amazonaws.${var.region}.ssm"
    vpc_endpoint_type   = "Interface"
    private_dns_enabled = true
    vpc_id              = aws_vpc.vpc.id
    subnet_ids          = [
                          aws_subnet.private-subnet-a.id,
                          aws_subnet.private-subnet-b.id
    ]
    security_group_ids  = [
                          aws_security_group.linux-security-group.id,
                          aws_security_group.windows-security-group.id
    ]
    tags = {
        Name = "${var.project-name}-SSM-Endpoint"
  }
}

resource "aws_vpc_endpoint" "ssm-message-interfave-endpoint" {
    service_name        = "com.amazonaws.${var.region}.ssmmessages"
    vpc_endpoint_type   = "Interface"
    private_dns_enabled = true
    vpc_id              = aws_vpc.vpc.id
    subnet_ids          = [
                          aws_subnet.private-subnet-a.id,
                          aws_subnet.private-subnet-b.id
    ]
    security_group_ids  = [
                          aws_security_group.linux-security-group.id,
                          aws_security_group.windows-security-group.id
    ]
    tags = {
        Name = "${var.project-name}-SSMMessages-Endpoint"
  }      
}
