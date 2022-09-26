data "aws_ami" "latest-amazon-linux2-ami" {
    most_recent = true
    owners      = ["amazon"]

    filter {
        name   = "name"
        values = [var.image-name-linux]
    }    
    filter {
    name       = "virtualization-type"
    values     = ["hvm"]
    }   
}

data "aws_ami" "latest-windows-2019-ami" {
    most_recent = true
    owners      = ["amazon"]

    filter {
        name   = "name"
        values = [var.image-name-windows]
    }
    filter {
        name   = "virtualization-type"
        values = ["hvm"]
    }   
}

resource "aws_instance" "windows-a" {
    ami                  = data.aws_ami.latest-windows-2019-ami.id
    security_groups      = [var.security-group-windows]
    subnet_id            = var.subnet-a-id
    iam_instance_profile = aws_iam_instance_profile.ec2-instance-profile.id
    instance_type        = var.instance-type

    tags = {
        Name = "${var.project-name}-EC2-A-Windows"
  }    
}

resource "aws_instance" "windows-b" {
    ami                  = data.aws_ami.latest-windows-2019-ami.id
    security_groups      = [var.security-group-windows]
    subnet_id            = var.subnet-b-id
    iam_instance_profile = aws_iam_instance_profile.ec2-instance-profile.id
    instance_type        = var.instance-type

    tags = {
        Name = "${var.project-name}-EC2-B-Windows"
  }    
}

resource "aws_instance" "linux-a" {
    ami                  = data.aws_ami.latest-amazon-linux2-ami.id
    security_groups      = [var.security-group-linux]
    subnet_id            = var.subnet-a-id
    iam_instance_profile = aws_iam_instance_profile.ec2-instance-profile.id
    instance_type        = var.instance-type

    tags = {
        Name = "${var.project-name}-EC2-A-Linux"
  }    
}

resource "aws_instance" "linux-b" {
    ami                  = data.aws_ami.latest-amazon-linux2-ami.id
    security_groups      = [var.security-group-linux]
    subnet_id            = var.subnet-b-id
    iam_instance_profile = aws_iam_instance_profile.ec2-instance-profile.id
    instance_type        = var.instance-type

    tags = {
        Name = "${var.project-name}-EC2-B-Linux"
  }    
}

resource "aws_iam_role" "ec2-instances-role" {
    name = "${var.project-name}-EC2-Instances-role"
    path = "/"
    
    assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Sid       = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

    inline_policy {
        name = "SessionManagerRole"

        policy = jsonencode({
            Version   = "2012-10-17"
            Statement = [
                {
                    Action   = [
                                "ssm:DescribeAssociation",
                                "ssm:DescribeAssociation",
                                "ssm:GetDeployablePatchSnapshotForInstance",
                                "ssm:GetDocument",
                                "ssm:DescribeDocument",
                                "ssm:GetManifest",
                                "ssm:GetParameter",
                                "ssm:GetParameters",
                                "ssm:ListAssociations",
                                "ssm:ListInstanceAssociations",
                                "ssm:PutInventory",
                                "ssm:PutComplianceItems",
                                "ssm:PutConfigurePackageResult",
                                "ssm:UpdateAssociationStatus",
                                "ssm:UpdateInstanceAssociationStatus",
                                "ssm:UpdateInstanceInformation",
                                "ssmmessages:CreateControlChannel",
                                "ssmmessages:CreateDataChannel",
                                "ssmmessages:OpenControlChannel",
                                "ssmmessages:OpenDataChannel" 
                    ]
                    Effect   = "Allow"
                    Resource = "*"
                },
            ]
        })          
    }
}

resource "aws_iam_instance_profile" "ec2-instance-profile" {
    name = "${var.project-name}-EC2-Instance-Profile"
    path = "/"
    role = aws_iam_role.ec2-instances-role.name
}
