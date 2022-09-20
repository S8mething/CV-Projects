# <p align="center">Nextcloud</p>

<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/99510843/191354454-7dc2593b-2c46-4f7d-b3ff-dea6e6532e7a.png">
</p>

## Tools used:

- Amazon EC2  
- Amazon EFS  
- Docker
- Amazon Route 53

## Steps:

- Create 2 security groups for EC2 Instance and EFS

###### EC2 Instance Security Group. 81 port for nginx proxy manager configuration. 2049 for EFS Group

![image](https://user-images.githubusercontent.com/99510843/176520829-eb3a7e4b-eed7-49ab-a493-017c863edcf8.png)

###### EFS Security group

![image](https://user-images.githubusercontent.com/99510843/176521590-524e1c8b-bdbc-44ce-adbd-5546cc824da0.png)

- Create EFS for storage with EFS Security Group

![image](https://user-images.githubusercontent.com/99510843/176522736-73967854-271f-49d3-8659-60e523493ea3.png)

- Launch EC2 instance, mount EFS

- Register domain with Route 53 and create A record

![image](https://user-images.githubusercontent.com/99510843/176529437-540ed275-8d17-4349-b026-15c5bc89f029.png)

- Connect to EC2 instance with SSH and install docker and docker-compose, create network nextcloud containers

```
sudo apt-get -y install docker.io docker-compose
sudo docker network create nextcloud_network
```
- Create folder for Nextcloud storage

```
cd /mnt/efs/fs1
mkdir nextcloud
```
- Copy the Docker-Compose Template to your remote server. Execute the Docker-Compose file. ```docker-compose.yaml``` file and environment variables ```.env``` file to ```nextcloud``` folder
```
docker-compose up -d
```
- Check if all Containers are running properly
```
docker-compose ps
```
![image](https://user-images.githubusercontent.com/99510843/176534099-94073073-9d9f-481a-bc0e-b9bed877202e.png)

- Configure Nginx Proxy Manager
###### Connect to IP of EC2 instance with 81 port and first login credentials ```admin@example.com``` and password ```changeme```

- Add proxy host and Obtain a new SSL certificate with letsencrypt.

![image](https://user-images.githubusercontent.com/99510843/176535985-fd0d8874-153b-408f-9f47-3bfcb5b26b1d.png)
![image](https://user-images.githubusercontent.com/99510843/176536037-29937b71-fc0e-4cbd-9edf-f30e5b2921de.png)

- Connect to Nextcloud using host name and setup admin profile

![image](https://user-images.githubusercontent.com/99510843/176536370-601b10ae-3496-4681-86a8-5a6d8dbab278.png)







