# <p align="center">Python</p>


### <p align="center">[AWS EC2 monitoring and creating/deleting snapshots](https://github.com/S8mething/projects/tree/main/Python/Monitoring_and_Snapshots)</p>

<p align="center">
  <img width="850" height00" src="https://user-images.githubusercontent.com/99510843/188332776-09a89801-ffaf-4281-9100-1a523b0fb7f7.png">
</p>

#### Tools used:

- Python,
- AWS CloudFormation,
- AWS EC2,
- Slack

```cloudformation-stack.yaml``` - Template for creating resources in eu-north-1(Stockholm) and eu-west-3(Paris).

#### ***Scripts do:***
- ```ec2_status_check.py``` - Checks Stockholm(eu-north-1) and Paris(eu-west-3) EC2 Instance statuses, system state and instance state. Send Alerts or notifications to slack channels, saves logs to file.

![image](https://user-images.githubusercontent.com/99510843/188333075-08481fcd-4ef8-44fa-8921-c54a0a8b5a07.png)

- ```auto_creating_and_removing_snapshots.py``` - Creates snapshots on schedule, deletes all snapshots except two last. Send Alerts or notifications to slack channels, saves logs to file.

  - Success:
![image](https://user-images.githubusercontent.com/99510843/188333037-fe5b22e8-d5c5-47e8-a32d-e1d476997b03.png)

  - Error:
![image](https://user-images.githubusercontent.com/99510843/188332636-986f45bb-1382-4465-b057-5b70e635c72a.png)

- ```slack_sender.py``` - Slack handler. Saves logs of all messages or errors to file.
- ```logging_config.py``` - Python logging config dictionary.

### <p align="center">[Monitoring Nginx Web-Server](https://github.com/S8mething/projects/tree/main/Python/Monitoring_website)</p>

<p align="center">
  <img width="1000" height="370" src="https://user-images.githubusercontent.com/99510843/190897018-f1cda6d7-e63b-4c68-9670-41d49b17a785.png">
</p>

#### Tools used:

- Python,
- AWS CloudFormation,
- AWS EC2,
- Nginx docker container
- Slack

```cloudformation-stack.yaml``` - Template for creating resources.

#### ***Scripts do:***
- ```monitor_website.py``` - Monitors responce code of Nginx web-server. If code not 200 connects to EC2 Instance and restarts docker container. If response status code is unreachable, restarts EC2 Instance. All messages sends to slack channel.
  - Slack messages:
  ![2022-09-18_00-12](https://user-images.githubusercontent.com/99510843/190897238-4da53f6a-2ccc-4d22-a94a-ba9b2e7ef4d5.jpeg)

- ```slack.py``` - Slack handler. Saves logs of all messages or errors to file.
- ```logging_config.py``` - Python logging config dictionary.


### <p align="center">[Excel scripts](https://github.com/S8mething/projects/tree/main/Python/Excel_scripts)</p>

#### Tools used:

- Python,
- Microsoft Excel

####  ***Scripts do:***
- ```inventory-script.py```
  - List each company with respective product count.
  - List products with inventory less than 10.
  - List each company with respective total inventory Value.

  ![image](https://user-images.githubusercontent.com/99510843/188335225-79b6de9f-f57f-44c0-bebf-784be1b596b3.png)
  
  - Write to Excel: Calculate and write inventory value for each product into spreadsheet.

  ![image](https://user-images.githubusercontent.com/99510843/188334982-c80c4ac6-c62c-4e18-b592-7d222b1a06ea.png)

- ```employees.py```
  - Sorts by years of experience in descending order.
  - Creates chart.
  - Saves to another excel file.
  
    - ```employees.xlsx```
  
  ![image](https://user-images.githubusercontent.com/99510843/190896603-719d7076-4d34-4826-884d-d974ef2fb05f.png)

    - ```employees_sorted.xlsx```
    
  ![image](https://user-images.githubusercontent.com/99510843/190896629-0fe68bac-5eb0-4200-b724-7bdd9fd86d83.png)

  
  
  


