output "vpc-id" {
    description = "The ID of the VPC"
    value       = aws_vpc.vpc.id
}

output "linux-security-group-id" {
    description = "The ID of the Linux Security Group"
    value       = aws_security_group.linux-security-group.id
}

output "windows-security-group-id" {
    description = "The ID of the Windows Security Group"
    value       = aws_security_group.windows-security-group.id
}

output "private-subnet-a-id" {
    description = "The ID of the Private Subnet A"
    value       = aws_subnet.private-subnet-a.id
}

output "private-subnet-b-id" {
    description = "The ID of the Private Subnet B"
    value       = aws_subnet.private-subnet-b.id
}


