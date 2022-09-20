# <p align="center">CI-CD with Jenkins, Ansible, EKS</p>

<p align="center">
  <img width="1200" height00" src="https://user-images.githubusercontent.com/99510843/186012311-f3a226f3-5da8-4a1b-951a-c56bc5800bd4.png">
</p>

## Tools used:

- Ansible                                    
- Jenkins
- Gitlab
- AWS ECR  
- AWS EKS
- AWS CloudFormation
- Docker
- regapp on Tomcat [Project Gitlab link](https://gitlab.com/S8mething/reg-app-public.git)

                                   
#### ***Prerequisites for Jenkins server after creating Cloudformation Stack:***

#### **installed suggested Jenkins plugins and plugins below. Added AWS credentials and Git(Gitlab) credentials or ssh key, or token(if needed):**
> #### Publish over SSH plugin
> #### SSH Agent for Ansible server
> #### Smee.io link for proxy webhooks                                    
                                    
#### ***Prerequisites for Ansible server:***
                                    
#### **installed tools on Ansible server (installed automatically with cloudformation stack):**
                                   
> ##### Docker 
> ##### AWS CLI                   
> ##### kubectl  
> ##### pip3 packages: kubernetes 11.0.0, docker, openshift, boto3
> ##### java                                    


## Steps:

- Create 3 KeyPairs for EKS-Nodes, Jenkins and Ansible servers

![image](https://user-images.githubusercontent.com/99510843/185901538-9b82ba52-e1d2-4b40-ac89-650e6e6c9923.png)

- Create cloudformation stack 

![image](https://user-images.githubusercontent.com/99510843/191112556-b6486695-ed10-4740-b39c-c0db6eaba811.png)

- Login to Jenkins server, create ssh keypair and configure Publish over SSH plugin for connection to Ansible server. Add public key to Ansible

![image](https://user-images.githubusercontent.com/99510843/185904648-de80f9de-fec5-42a4-8762-46d0dcaff62f.png)
                                    
![image](https://user-images.githubusercontent.com/99510843/185908915-583de1fc-fdd3-494a-9088-c695106eeb4d.png)
                                    
![image](https://user-images.githubusercontent.com/99510843/185909038-0f80fa4c-9755-42f2-9120-f0bde612f109.png)
                                    

- Ansible server ```authorized_keys```
                                  
![image](https://user-images.githubusercontent.com/99510843/185905866-f5c26823-cac6-4bcb-af10-eb29c4426b21.png)
                                    
- Ansible server ```aws configure```
                                    
![image](https://user-images.githubusercontent.com/99510843/185909889-f376dbd9-bd91-4c5e-9b0e-9fe77e2a8863.png)
                                    
- Download configuration for EKS Cluster on Ansible server ```aws eks update-kubeconfig --name RegApp-EKS```  

![image](https://user-images.githubusercontent.com/99510843/185912091-7a87709a-d58e-4332-bf6c-8b0ad2492d43.png)
                                    
- Add Ansible ssh credentials and create Agent for execution ansible commands 

![image](https://user-images.githubusercontent.com/99510843/185929560-7263ac38-ecef-48a9-92bc-f96612865ec1.png)                            
                                                                  
- Create Jenkins Pipline Job from Jenkinsfile
                                    
![image](https://user-images.githubusercontent.com/99510843/185947918-724e0ac4-ce18-4f96-8599-0f9ee9d028ab.png)                                   
                                    
- Connect to regapp page via ELB

![image](https://user-images.githubusercontent.com/99510843/185930920-3c6c17dd-c62e-4d55-9655-9c19e1497807.png)
                                    
![image](https://user-images.githubusercontent.com/99510843/185931099-422a61ae-b0b0-40ba-b060-f2c52a0ddad1.png)
                                    
- regapp deployment status                                    

![image](https://user-images.githubusercontent.com/99510843/185931259-dbc41576-ed60-4ca3-ba01-3c057973d3c4.png)
                                    
- Add webhook for Jenkins pipline using webhook proxy service [smee.io](https://smee.io)    
                                    
![image](https://user-images.githubusercontent.com/99510843/185948674-dfc9422a-5d59-4a49-b00e-576e2d3eb9e4.png)

- Add redirection ```smee -u https://smee.io/yf0kzvUFEukgYYp --path /project/regapp-pipeline/ --port 8080```
                                    
- Add webhook in Gitlab, Enable webhook trigger in Jenkins and create access token
                                    
![image](https://user-images.githubusercontent.com/99510843/185949409-f1c818a2-7f48-4f6c-b475-d166877e552c.png)

![image](https://user-images.githubusercontent.com/99510843/185949483-886b5d06-6c02-48a1-bf82-8cd776179da0.png)

![image](https://user-images.githubusercontent.com/99510843/185949593-43bafb3a-df8f-48de-91b0-a93dd6b48562.png)

- Test CI-CD. Update ```vars.yaml``` for deployment new version of regapp

![image](https://user-images.githubusercontent.com/99510843/185950122-2e705dd1-e436-4ed2-b4e4-2869d401ad57.png)
                                    
![image](https://user-images.githubusercontent.com/99510843/185950310-b00d8355-7d8f-4646-bb1e-0fa684056172.png)

![image](https://user-images.githubusercontent.com/99510843/185950477-6bdf51cf-a83a-4241-8b80-a2e1d4a657d9.png)

- Smee responce
                                    
![image](https://user-images.githubusercontent.com/99510843/185950841-87c24a68-546f-460d-b380-de581a28a820.png)
                                    
- Jenkins build
                                    
![image](https://user-images.githubusercontent.com/99510843/185951170-8b7360e1-cc8a-4621-b9c9-4bd80d40d611.png)

- Deployment on EKS

![image](https://user-images.githubusercontent.com/99510843/185951486-f2adcb24-dc66-482b-95b3-2b24ff5e7725.png)

- ELB link
                                    
![image](https://user-images.githubusercontent.com/99510843/185951658-e81242d8-ae79-4ffa-94b9-327246b03062.png)
                                    
                                    
                                    

                                    
                                   
                                    
                                    
                                    
                                    

                                    
                                    

