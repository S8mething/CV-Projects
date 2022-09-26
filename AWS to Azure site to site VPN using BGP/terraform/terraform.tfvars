project-name       = "AWS-to-Azure"
region             = "eu-north-1"
cidr-block-vpc     = "192.168.0.0/16"
cidr-block-subnet  = [
                      "192.168.0.0/24",
                      "192.168.16.0/24"
]
availability-zone  = [
                      "eu-north-1a",
                      "eu-north-1b"
]
azure-cidr-block   = "10.1.0.0/16"
instance-type      = "t3.micro"
image-name-linux   = "amzn2-ami-kernel-*-hvm-*-x86_64-gp2" 
image-name-windows = "Windows_Server-2019-English-Full-Base-*"
 
