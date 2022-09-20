# <p align="center">AWS to Azure site to site VPN using BGP</p>

<p align="center">
  <img width="1200" height00" src="https://user-images.githubusercontent.com/99510843/191260326-4a13898a-458a-4b43-82c5-634a3944cdbf.png">
</p>

## Tools used:

- AWS VPC  
- AWS EC2
- AWS CloudFormation
- AWS Session Manager
- Azure Virtual Machine
- Azure Virtual Network Gateway


## Steps:

###### AWS:

- Create CloudFormation Stack and upload template:

![1](https://user-images.githubusercontent.com/99510843/178160441-290f595e-fdfa-4353-ba9c-cbfad505d6d2.jpeg)

![2](https://user-images.githubusercontent.com/99510843/178160454-504e0a9d-b35c-4275-8f14-e51927b7715d.jpeg)

###### Microsoft Azure:

- Create new resourse group for project

- Create Virtual Network and subnet for Virtual Machine

![3](https://user-images.githubusercontent.com/99510843/178160513-9fed61f0-e095-46ab-929d-235366a81496.jpeg)

- In Virtual Network create GatewaySubnet for Virtual network gateway:

![5](https://user-images.githubusercontent.com/99510843/178160556-e248bb36-b098-4748-8353-bac91c8f67bc.jpeg)

- Create Virtual network gateway:
  - Gateway type: VPN
  - VPN type: Route-based
  - SKU: VpnGw2
  - Generation: Generation 2
  - Virtual network: ```Network-Name```
  - Enable active-active mode: Enabled
  - Configure BGP: Enabled
  - Autonomous system number (ASN): ```65000``` 
  ***This ASN must be different than the ASN used by AWS.***
  - Custom Azure APIPA BGP IP address: ```169.254.21.2, 169.254.22.2```
  - Second Custom Azure APIPA BGP IP address: ```169.254.21.6, 169.254.22.6```


![6](https://user-images.githubusercontent.com/99510843/178160689-767154d0-7b81-4b9c-a4ca-e302fc5bb853.jpeg)

![7](https://user-images.githubusercontent.com/99510843/178160951-99f09a82-df2c-42c6-8fb1-4604ec35fdfe.jpeg)

- Use two public IP Adresses for creating Customer Gateway in ```AWS```:

![8](https://user-images.githubusercontent.com/99510843/178161114-de8fed49-8814-4b10-b69c-869480ee65e9.jpeg)

###### AWS:

- Create two Customer gateways:

![9](https://user-images.githubusercontent.com/99510843/178161130-56df692a-ba65-442b-81c1-317c9660499b.jpeg)

![10](https://user-images.githubusercontent.com/99510843/178161135-17c96f26-f60a-402e-b512-3b2978dd198e.jpeg)

- Create two VPN Transit Gateway Attachments for both customer gateways:
  - First VPN:
    - Local IPv4 Network CIDR: ```0.0.0.0/0```  
    - Inside IPv4 CIDR for Tunnel 1: ```169.254.21.0/30```
    - Inside IPv4 CIDR for Tunnel 2: ```169.254.22.0/30```
  - Second VPN:
    - Local IPv4 Network CIDR: ```0.0.0.0/0``` 
    - Inside IPv4 CIDR for Tunnel 1: ```169.254.21.4/30```
    - Inside IPv4 CIDR for Tunnel 2: ```169.254.22.4/30```  

![11](https://user-images.githubusercontent.com/99510843/178161145-68863724-adb2-4437-b175-0a59b582b435.jpeg)

![12](https://user-images.githubusercontent.com/99510843/178161155-3bb063ca-c61c-4c64-a93c-4add01fcfea1.jpeg)

- Download both configurations with Generic vendor:

![14](https://user-images.githubusercontent.com/99510843/178161387-dedc5e6c-101e-4ac0-a041-8d279e62115e.jpeg)

- For next steps need information from configuration text files:

  - VPN-A:
    - Tunnel 1 Pre-Shared Key  
    - Tunnel 1 (Virtual Private Gateway) Outside IP address
    - Tunnel 1 Neighbor IP Address
     
    - Tunnel 2 Pre-Shared Key B 
    - Tunnel 2 (Virtual Private Gateway) Outside IP address 
    - Tunnel 2 Neighbor IP Address

  - VPN-B: 
    - Tunnel 1 Pre-Shared Key  
    - Tunnel 1 (Virtual Private Gateway) Outside IP address 
    - Tunnel 1 Neighbor IP Address 
    
    - Tunnel 2 Pre-Shared Key 
    - Tunnel 2 (Virtual Private Gateway) 
    - Tunnel 2 Neighbor IP Address
    
###### Microsoft Azure:

- Create 4 local network gateways:
  - Local network gateway for VPN-A Tunnel 1: 
    - Ip Adress = ```Tunnel 1 (Virtual Private Gateway) Outside IP address```
    - ASN = ```AWS ASN```
    - BGP peer Adress = ```Tunnel 1 Neighbor IP Address``` 
  - Local network gateway for VPN-A Tunnel 2
    - Ip Adress = ```Tunnel 2 (Virtual Private Gateway) Outside IP address```
    - ASN = ```AWS ASN```
    - BGP peer Adress = ```Tunnel 2 Neighbor IP Address```
  - Local network gateway for VPN-B Tunnel 1:
    - Ip Adress = ```Tunnel 1 (Virtual Private Gateway) Outside IP address```
    - ASN = ```AWS ASN```
    - BGP peer Adress = ```Tunnel 1 Neighbor IP Address```
  - Local network gateway for VPN-B Tunnel 2:
    - Ip Adress = ```Tunnel 2 (Virtual Private Gateway) Outside IP address```
    - ASN = ```AWS ASN```
    - BGP peer Adress = ```Tunnel 2 Neighbor IP Address```

![15](https://user-images.githubusercontent.com/99510843/178161645-70f87ae3-b23e-4dd6-953e-f6ad5db243b2.jpeg)

![16](https://user-images.githubusercontent.com/99510843/178161649-f971bdf5-abfe-4f15-8fc5-a02dfcd682d9.jpeg)

![17](https://user-images.githubusercontent.com/99510843/178161652-7b3b721e-2257-419a-af3f-825b6a2dc2a3.jpeg)

- In Virtual network gateway add 4 Connections for each local network gateway:

  - Tunnel-1-VPN-A1:
    - Local network gateway = ```Local network gateway for VPN-A Tunnel 1```
    - Enable BGP, then Enable Custom BGP Addresses
    - Primary Custom BGP Address = ```169.254.21.2```
    - Secondary Custom BGP Address = ```169.254.21.6 ```
    - Shared key (PSK) = ```Tunnel 1 Pre-Shared Key```
    - IKE Protocol = ```IKEv2```
  - Tunnel-2-VPN-A2:
    - Local network gateway = ```Local network gateway for VPN-A Tunnel 2```
    - Enable BGP, then Enable Custom BGP Addresses
    - Primary Custom BGP Address = ```169.254.22.2```
    - Secondary Custom BGP Address = ```169.254.21.6```
    - Shared key (PSK) = ```Tunnel 2 Pre-Shared Key```
    - IKE Protocol = ```IKEv2```
  - Tunnel-1-VPN-B1:
    - Local network gateway = ```Local network gateway for VPN-B Tunnel 1```  
    - Enable BGP, then Enable Custom BGP Addresses
    - Primary Custom BGP Address = ```169.254.21.2 ```
    - Secondary Custom BGP Address = ```169.254.21.6 ```
    - Shared key (PSK) = ```Tunnel 1 Pre-Shared Key```
    - IKE Protocol = ```IKEv2```
  - Tunnel-2-VPN-B1:
    - Local network gateway = ```Local network gateway for VPN-B Tunnel 2``` 
    - Enable BGP, then Enable Custom BGP Addresses
    - Primary Custom BGP Address = ```169.254.21.2 ```
    - Secondary Custom BGP Address = ```169.254.22.6 ```
    - Shared key (PSK) = ```Tunnel 2 Pre-Shared Key```
    - IKE Protocol = ```IKEv2```


![18](https://user-images.githubusercontent.com/99510843/178161909-e44529b7-11cb-4f3d-a5b5-3ff1025e1572.jpeg)

- Check status:

![19](https://user-images.githubusercontent.com/99510843/178162211-cffce508-688f-423a-a9c1-9d14a98a5c8a.jpeg)

- In Virtual network gateway check BGP peers connections:

![20](https://user-images.githubusercontent.com/99510843/178162578-5a01e24a-5d50-4f62-92a5-5f7ae58c104f.jpeg)

- Create Virtual Machine for testing

![22](https://user-images.githubusercontent.com/99510843/178162612-b0c97c8f-e1cd-4ff7-8e51-d677144c48dd.jpeg)

###### AWS:

- Check VPN Routes in AWS:

![21](https://user-images.githubusercontent.com/99510843/178162595-ac21b397-9e14-4743-a11c-2504ae63c8f3.jpeg)

- Connect with session manager to two Windows instances for changing Administrator password:

![24](https://user-images.githubusercontent.com/99510843/178162662-624807b2-6697-4788-9579-6ecf0d431d0e.jpeg)

![25](https://user-images.githubusercontent.com/99510843/178162664-24c82b31-0328-4568-a8f2-adea6837cc2a.jpeg)

- Install AWS CLI and AWS session Manager Plugin for connecting to private Windows instances via RDP with port-forwarding:

![26](https://user-images.githubusercontent.com/99510843/178162685-e06c8991-5d0f-462d-ae28-1e4b140b834c.jpeg)

- Start session manager session for one of windows instances:

![27](https://user-images.githubusercontent.com/99510843/178162726-640e8fab-8a76-49d9-98b2-5d2a0c29b8fa.jpeg)

- Connect using ```localhost:9999```

![28](https://user-images.githubusercontent.com/99510843/178162742-5560baec-a91d-4f4d-9d80-27adc6d06a3c.jpeg)

- ***(optional)*** By default on Windows Servers ICMP is deny, add firewall rule using Powershell for all Windows severs to allow ping:

![29](https://user-images.githubusercontent.com/99510843/178162812-6d3b7965-5320-4f63-a11f-a1b5d823bf5d.jpeg)

- Test RDP from ```AWS Instance to Azure VM```

![30](https://user-images.githubusercontent.com/99510843/178162888-98c58c76-7470-411d-b747-88d78e52d6ec.jpeg)

![31](https://user-images.githubusercontent.com/99510843/178162891-75aa7673-e200-4185-b8e7-d2d5784e9619.jpeg)

- Start session manager session for second of windows instances and test RDP to Azure VM:

![32](https://user-images.githubusercontent.com/99510843/178162921-dbac9541-52d4-4bd5-b00d-1e4d503386a8.jpeg)

![33](https://user-images.githubusercontent.com/99510843/178162924-7ab91ec6-f5da-4386-8f28-c572ae6cb97c.jpeg)

- Connect to first and second Linux instances and ping Azure VM:

![37](https://user-images.githubusercontent.com/99510843/178162947-5944adbe-9d69-4aa9-8b17-bd37f9b91a93.jpeg)

![38](https://user-images.githubusercontent.com/99510843/178162951-c96f96bd-a8f5-460b-85e9-9e5e5647097b.png)

###### Microsoft Azure:

- Configure network inbound rules for connecting only from MyIP and AWS VPC with RDP, and allow rule for ping only from AWS VPC:

![image](https://user-images.githubusercontent.com/99510843/178163205-b842c2c5-b462-41f2-8538-1e212ef73d20.png)


- Connect with public IP using RDP

![23](https://user-images.githubusercontent.com/99510843/178162642-f7f36f85-48ee-468b-bf91-282b74b1f47a.jpeg)

- Test RDP connection to AWS Windows Instances:

![34](https://user-images.githubusercontent.com/99510843/178162972-f98a87c3-c4ba-493d-960a-db72c1891e87.jpeg)

![35](https://user-images.githubusercontent.com/99510843/178162976-e6c1dc52-fe53-45d4-a006-2e315b714ca2.jpeg)

- Ping two Linux AWS instances:

![36](https://user-images.githubusercontent.com/99510843/178162986-0ba972d5-b61c-49c5-aa8c-550767b53520.jpeg)

***All connections works as they should***
















