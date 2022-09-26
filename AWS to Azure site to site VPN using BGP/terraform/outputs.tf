output "windows-a-private-ip" {
    value = module.instances.windows-a.private_ip
}

output "windows-b-private-ip" {
    value = module.instances.windows-b.private_ip  
}

output "linux-a-private-ip" {
    value = module.instances.linux-a.private_ip  
}

output "linux-b-private-ip" {
    value = module.instances.linux-b.private_ip  
}