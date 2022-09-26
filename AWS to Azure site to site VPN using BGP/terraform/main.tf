provider "aws" {
    region = var.region
}

module "vpc" {
    source            = "./modules/vpc"
    region            = var.region
    project-name      = var.project-name
    cidr-block-vpc    = var.cidr-block-vpc
    cidr-block-subnet = var.cidr-block-subnet             
    availability-zone = var.availability-zone
    azure-cidr-block  = var.azure-cidr-block              
}

module "instances" {
    source                 = "./modules/instances"
    project-name           = var.project-name
    instance-type          = var.instance-type
    image-name-linux       = var.image-name-linux
    image-name-windows     = var.image-name-windows
    security-group-linux   = module.vpc.linux-security-group-id
    security-group-windows = module.vpc.windows-security-group-id
    subnet-a-id            = module.vpc.private-subnet-a-id
    subnet-b-id            = module.vpc.private-subnet-b-id
}