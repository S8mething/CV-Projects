# <p align="center">Microservice app on EKS Cluster</p>


<p align="center">
  <img width="1200" height00" src="https://user-images.githubusercontent.com/99510843/184543768-38c33268-4cce-4ca9-b75c-f53d17ad4271.png">
</p>

## Tools used:

- Jenkins
- Gitlab
- AWS ECR  
- AWS EKS
- AWS CloudFormation
- AWS Cloudwatch
- AWS Route53
- Docker
- Microservices app online boutique [My Project Gitlab link](https://gitlab.com/S8mething/butique-app-public.git)
- Helm
- Helmfile
- Istio service mesh
- eksctl
                                   
#### ***Prerequisites for Jenkins server:***

#### **installed suggested Jenkins plugins and plugins below. Added AWS credentials and Git(Gitlab) credentials or ssh key, or token(if needed):**
> ##### Pipeline: AWS Steps Plugin
> ##### CloudBees AWS Credentials Plugin
#### **installed tools:**
> ##### Docker
> ##### AWS CLI                                 
> ##### kubectl
> ##### Helm
> ##### Helmfile
> ##### eksctl


## Steps:
                                   
- Create KeyPair for EKS Nodes(optional) and certificate in ACM for ALB, add record to Route53:

![image](https://user-images.githubusercontent.com/99510843/184543276-7ee9d6cb-1690-4d9c-a59f-88e48cc8e425.png)

- Create Pipline job in Jenkins, add Jenkinsfile or copy code.
                                   
- Edit in Jenkinsfile global variables:
  - ```ACCOUNT_ID```= "AWS account ID"
  - ```REGION```= "AWS Region ID"
  - ```PROJECT_NAME```= "Project name for ECR Repositories"
  - ```TAG```= "Tag for images"
  - ```AWS_CLOUDFORMATION_STACK_NAME```= "AWS Cloudformation stack name"
  - ```DOMAIN_NAME```= "Domain name"
  - ```CERTIFICATE_ARN```= "ARN of certificate from ACM"
  - ```AMAZON_ECR```= "Amazon ECR link, using for pulling images from Amazon repositories, list [Amazon container image registries](https://docs.aws.amazon.com/eks/latest/userguide/add-ons-images.html)"
  - ```KEYNAME```= "SSH KeyName for SSH access to nodes if needed"    
                                                                  
- Build Jenkins Project:

![image](https://user-images.githubusercontent.com/99510843/184544641-e790a5f3-7ebb-46fe-a434-d2b659ef8c45.png)

- Add alias record in Route53 to ALB:

![image](https://user-images.githubusercontent.com/99510843/184544303-9ca9cca6-acbe-444d-9cd7-26715a21b1e6.png)

- Visit domain and check availability of app:

![image](https://user-images.githubusercontent.com/99510843/184544393-83c938f0-4dcf-4fe4-9c95-78743e7810f4.png)

- Deployment status:

![image](https://user-images.githubusercontent.com/99510843/184551592-9a0e7eee-a8ed-4aa9-ab37-3c23befc5c9a.png)

![image](https://user-images.githubusercontent.com/99510843/184551654-b618fb32-dccf-48e3-92e9-4c4ba75498d8.png)

- Install few addons for istio:

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.14/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.14/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.14/samples/addons/kiali.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.14/samples/addons/jaeger.yaml
```

- Kiali dashboard:

![image](https://user-images.githubusercontent.com/99510843/184551873-e1a77485-470a-4160-8b13-e60455296ad0.png)




[Original Project from Google](https://github.com/GoogleCloudPlatform/microservices-demo) 
