# <p align="center">Jenkins to AWS ECS Spring-boot Petclinic APP</p>

<p align="center">
  <img width="900" src="https://user-images.githubusercontent.com/99510843/182145519-fbac6819-600b-44e4-9559-533aa5c78c71.png">
</p>

## Tools used:

- Jenkins
- Gitlab
- AWS ECR  
- AWS ECS
- AWS CloudFormation
- AWS Systems Manager Parameter Store
- AWS Cloudwatch
- AWS SNS
- AWS RDS MySQL
- AWS Certificate Manager
- AWS Route53
- AWS CLI
- Docker
- Azure Virtual Machine
- Springboot Petclinic App
- phpMyAdmin docker container

## VPC Endpoints:

- .s3  - gateway
- .ecs-telemetry
- .logs
- .ssm
- .ecr.api
- .ecr.dkr
- .ecs
- .ecs-agent


###### Description ```task-blueprint.sh```

***Blueprint can be used with other piplines. Used to check the revision and send messages about the result success or failure. Can be modified if need by adding some new variables such as topic name.***

## Steps:

###### Jenkins Azure Virtual Machine:

- GitLab https://gitlab.com/S8mething/spring-petclinic-public.git
- For Jenkins Server I used Azure Virtual Machine with suggested pluigins + GitLab.
- Install ```Docker```,```AWS CLI```, ```jq``` and add permissions to Jenkins user for Docker and AWS.
- After creation Jenkins user in AWS, configure AWS CLI.
- Create Pipline Project, add Pipline script or use Jenkinsfile.
- Add credentials, token or ssh-key to Gitlab(pub.key), privat-key to Jenkins for access to Gitlab(If project is private).

###### AWS:

- Create 3 Parameters in Systems Manager Parameter Store for MYSQL_USER and MYSQL_PASS for env variables petclinic container and for RDS Database Administrator password MySQLAdminPassParameterName

![image](https://user-images.githubusercontent.com/99510843/191110814-a2882b6b-391b-41be-8753-02919e07ce57.png)

- Create 2 topics with EMAIL verificated mails

![image](https://user-images.githubusercontent.com/99510843/181784434-d8ec2d03-e33d-4ebf-8b25-afa16bf49114.png)

- Create SSL sertificate and create records in Route53

![image](https://user-images.githubusercontent.com/99510843/181790600-538de3ec-8012-4cda-b79c-c5723d2afb47.png)

- Create User "Jenkins" with permissions
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:DeregisterTaskDefinition",
                "ecs:UpdateService",
                "ecs:UpdateCluster",
                "ecs:RunTask",
                "ecs:DescribeClusters",
                "ecs:RegisterTaskDefinition",
                "ecs:DescribeServices",
                "ecs:DescribeTasks",
                "ecs:DescribeTaskDefinition",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken",
                "ecr:UploadLayerPart",
                "ecr:InitiateLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "PassRole",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/Petclinic-ECSTask-Role"
        }
    ]
}
```
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": [
                "arn:aws:sns:eu-north-1:<YOUR_ACCOUNT_ID>:Jenkins-Success",
                "arn:aws:sns:eu-north-1:<YOUR_ACCOUNT_ID>:Jenkins-Failure"
            ]
        }
    ]
}
```

- Create Cloudformation stack with ```PetclinicStack.yaml``` template. Parameters:
  - ```AdminMySQLName``` ***Admin RDS MYSQL Name***
  - ```AmiEC2Id``` - ***Referense for image id from AWS Parameter Store for EC2 Instance***
  - ```AmiECSId``` - ***Referense for image id from AWS Parameter Store for ECS EC2 Instances***
  - ```CertificateARN```  ***Certificate ARN*** 
  - ```ECRepositoryName``` ***ECR Repository Name***
  - ```KeyNameECSEC2``` ***KeyPair name if SSH connection needed, by default ECS EC2 instances in private subnet***
  - ```KeyNamePHPEC2``` ***KeyPair name for phpMyAdmin EC2 Instance***
  - ```LogGroupName``` ***Name of LogGroup for petclinic app containers***
  - ```MySQLAdminPassParameterName``` ***Parameter Name from Parameter Store for Administrator RDS Database password***
  - ```MYSQLNameParameterARN``` ***Parameter Name from Parameter Store for MYSQL_USER environment variable***
  - ```MYSQLPassParameterARN``` ***Parameter Name from Parameter Store for MYSQL_PASS environment variable***


![image](https://user-images.githubusercontent.com/99510843/191109195-8355e21a-967f-47f0-be1b-2cdec8ad426c.png)

- Connect to PHP instance via publicIP or publicDNSName. Use Administrator credentials to create user for petclinic app ```Username=MYSQL_USER(NAME) parameter, password=MYSQL_PASS parameter```. Add permissions to petclinic database

![image](https://user-images.githubusercontent.com/99510843/181789415-22accbad-5a0d-4eb5-9c3f-d7eb021f4db9.png)

![image](https://user-images.githubusercontent.com/99510843/181789607-017eaedb-468f-4a26-9c09-1b9c5ca835e5.png)
![image](https://user-images.githubusercontent.com/99510843/181789905-97a85aab-2e0a-4161-8fde-8f0d30748a99.png)

- Use ```schema.sql``` and ```data.sql``` scripts add schema and data to petclinic database

- Add DNS Record with redirection to Application load balancer

![image](https://user-images.githubusercontent.com/99510843/181790939-1c9db3b6-968d-4139-ac57-c53eb931f7d0.png)

![image](https://user-images.githubusercontent.com/99510843/181790998-02c8d857-2f32-467b-9d10-2c6fb2e70b4a.png)

- Add HTTPS Listener to ALB

![image](https://user-images.githubusercontent.com/99510843/181791382-65d2dbbe-d307-435d-918f-761284c1f9d2.png)

###### Jenkins:

- Build Pipeline

![image](https://user-images.githubusercontent.com/99510843/181792093-2c66f01b-15f6-47c8-9a11-ed54e409173c.png)

- Check ECS Cluster

![image](https://user-images.githubusercontent.com/99510843/181792262-313117a4-6249-46b4-8ba0-ee943e072423.png)

- Test domain name connection

![image](https://user-images.githubusercontent.com/99510843/181792466-d3f69e31-1c35-419e-9893-29d5f0dc407b.png)

- Check Email

![image](https://user-images.githubusercontent.com/99510843/181793012-911a3463-f24a-43bb-9d1b-b6d124379b05.png)

- In Gitlab add Jenkins integration for automatic deployment

![image](https://user-images.githubusercontent.com/99510843/181792809-3d78ea82-add6-4460-9a34-e1a06f3131b6.png)

![image](https://user-images.githubusercontent.com/99510843/181794401-c4a9f4d4-61f3-4b4a-9208-396a90a21c14.png)

- Change version in Gitlab and test

![image](https://user-images.githubusercontent.com/99510843/181796067-cf474918-4e40-4afd-9931-bd306466e97a.png)

![image](https://user-images.githubusercontent.com/99510843/181796306-f2a50b4f-02dd-41bc-9f42-443d373ed50c.png)

![image](https://user-images.githubusercontent.com/99510843/181796382-f50cad25-b394-4965-8656-9583523bade8.png)

![image](https://user-images.githubusercontent.com/99510843/181829662-ba2eaf52-3ccf-4646-bb8e-60ca0ce33452.png)

![image](https://user-images.githubusercontent.com/99510843/181797228-bbe08658-cb52-48ea-b0d6-8c938531566f.png)

![image](https://user-images.githubusercontent.com/99510843/181798843-ea4474c2-97db-4050-8698-e0a04e48899d.png)

![image](https://user-images.githubusercontent.com/99510843/181798909-3fa25311-0dfd-4319-be00-43bd481e4e01.png)








[***Spring-boot Petclinic Original project link***](https://github.com/spring-projects/spring-petclinic)




