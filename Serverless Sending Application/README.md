# <p align="center">Serverless Sending Application</p>

<p align="center">
  <img width="750"  src="https://user-images.githubusercontent.com/99510843/176912464-88f1cb1b-ca35-41a7-82aa-d4709257f865.png">
</p>

## Tools used:

- AWS S3
- AWS API Gateway
- AWS Lambda
- AWS Step Functions
- AWS SNS
- AWS SES
- JS and Python 

## Steps:

- Create a Lambda Role 

![image](https://user-images.githubusercontent.com/99510843/176917629-59cc9858-7970-466f-981b-e26879de4afa.png)

- Create Identity in SES and add two emails, one for source and second for destination

![image](https://user-images.githubusercontent.com/99510843/176918872-a7528ba2-c9e6-47dc-9fb3-8d14e6664fc0.png)

###### After creating source and destination emails must be verified
![image](https://user-images.githubusercontent.com/99510843/176919942-dbf9a70e-dc34-4533-b08d-9d8c2a70da50.png)

- Create a Lambda function ```email``` with existing Lamdba Role 

![image](https://user-images.githubusercontent.com/99510843/176920710-60efb2b6-13b8-405c-8be1-6cea1e2d53ff.png)

###### Paste code from ```email.py```
![image](https://user-images.githubusercontent.com/99510843/176921281-234305ba-4746-49b8-b85a-f960ed42bcb3.png)

- Add phone number in SNS and verify it 

![image](https://user-images.githubusercontent.com/99510843/176923452-875ee9fd-500b-492e-b3c1-a7f30b08d699.png)

- Create a Lambda function capable of sending to SNS the instruction to send a SMS

![image](https://user-images.githubusercontent.com/99510843/176923929-e5ccfb7f-5353-49cf-aec4-ec210b1abe52.png)

###### Paste code from ```sms.py```
![image](https://user-images.githubusercontent.com/99510843/176924145-ef001e86-7386-4325-94c6-aef7c34500d3.png)

- Create Sending State Machine in AWS Stepfunction

![image](https://user-images.githubusercontent.com/99510843/176924354-131e58ea-916f-45fb-9cab-a387a405be2c.png)
![image](https://user-images.githubusercontent.com/99510843/176924380-abb073e5-bed7-4ee2-be17-afd34e54ee9d.png)
![image](https://user-images.githubusercontent.com/99510843/176924409-bf8777a6-799e-4ddb-a2d6-7ecf1c257cb3.png)

Paste code from ```stateMachineSending.json``` and add the ARNs of the Lambda functions email.py and sms.py to the corresponding states
```
{
    "Comment": "State machine for sending SMS & email",
    "StartAt": "Select Type of Sending",
    "States": {
        "Select Type of Sending": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.typeOfSending",
                    "StringEquals": "email",
                    "Next": "Email"
                },
                {
                    "Variable": "$.typeOfSending",
                    "StringEquals": "sms",
                    "Next": "SMS"
                }
            ]
        },
        "Email": {
            "Type" : "Task",
            "Resource": "<lambda_email.py_arn>",
            "End": true
        },
        "SMS": {
            "Type" : "Task",
            "Resource": "<lambda_sms.py_arn>",
            "End": true
        }
    }
}
```

- Create Lambda Function restApiHandler.py

![image](https://user-images.githubusercontent.com/99510843/176925267-28c27633-054c-4ec1-b1a3-b8a7e081f1ab.png)

###### Paste code from ```restApiHandler.py``` and add state machine ARN
![image](https://user-images.githubusercontent.com/99510843/176925726-ba3dfec1-7a04-4f46-a772-0e62cd6988d7.png)

- Create a REST API using API Gateway

![image](https://user-images.githubusercontent.com/99510843/176960466-5df21f55-bd81-4676-bf62-f8d18532534e.png)

- Create Resource

![image](https://user-images.githubusercontent.com/99510843/176960536-6115b973-3442-4951-b9bf-caff3217034b.png)

- Create POST Method

![image](https://user-images.githubusercontent.com/99510843/176960642-0aa6d28c-8093-4c74-8dae-5fecd59d19da.png)

- Deploy API

![image](https://user-images.githubusercontent.com/99510843/176960753-8a172ef4-cf8c-439c-a092-756cfe2333f1.png)

- Copy invoke URL https://YOUR-URL.amazonaws.com/sendingStage/sending and paste it to ```formToApi.js```

- Create S3 bucket

- Upload the website on S3

![image](https://user-images.githubusercontent.com/99510843/176961869-e021aa8d-2b9a-4937-9155-724d41170690.png)

- Edit Permissions for public access

![image](https://user-images.githubusercontent.com/99510843/176961925-0bcd82cf-8f52-4373-ba43-5391504822ee.png)

- Edit bucket policy 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::bucket_name/*"
            ]
        }
    ]
}
```

- Enable static website hosting

![image](https://user-images.githubusercontent.com/99510843/176962103-bc8902b9-b57d-4f45-8821-0983d41584a2.png)

- Open website URL and test Email % SMS

![image](https://user-images.githubusercontent.com/99510843/176962290-e6ccba38-d6fd-40fc-9007-7f1125dfc2f4.png)

![image](https://user-images.githubusercontent.com/99510843/176962329-a5f8653c-146f-467d-a718-2fb44955dbd1.png)

![image](https://user-images.githubusercontent.com/99510843/176962498-bffde84a-c12b-41d2-865b-8554667e951a.png)













