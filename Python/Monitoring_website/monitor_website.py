import requests
import paramiko
import time
import logging
import boto3
import schedule
from sys import stderr, stdout
from logging_config import LOGGING_CONFIG
from slack import slack_sender
from botocore.exceptions import ClientError
from requests.exceptions import RequestException

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('monitoring_logger')

host = 'http://13.50.69.25'
host_ip = '13.50.69.25'
key_file = paramiko.RSAKey.from_private_key_file('website_key.pem')
active_responce = 200
container_name = 'website'
ec2_client = boto3.client('ec2')
boto_error = str
responce_error = False

def reboot_webserver():
    global boto_error
    response = ec2_client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'Web-Server'
            ]
        },
    ])
    try:
        instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
        ec2_client.reboot_instances(
        InstanceIds=[
            instance_id,
        ])
        time.sleep(45)
        for attempts in range(5):
            responce = requests.get(host)
            emojipic = emoji(responce.status_code)           
            state = response['Reservations'][0]['Instances'][0]['State']['Name']
            if state == 'running':
                slack_sender(f'Web-Server rebooted successfully.:white_check_mark:\nApplication status code {responce.status_code} {emojipic}')
                logger.info(f'Web-Server rebooted successfully.')
                break  
            else:
                if attempts == 5:
                    slack_sender(f'Web-Server state is {state}.:heavy_exclamation_mark:')
                    logger.error(f'Web-Server state is {state}.')
                    break
                else:
                    time.sleep(20)                                
    except ClientError as error:
        if error.response['Error']['Code'] == boto_error:
            pass      
        else:
            boto_error = error.response['Error']['Code']
            message = error.response['Error']['Message']
            slack_sender(f'Botocore error code: {boto_error}.\n Error message: {message}:x:')
            logger.error(f'Botocore error code: {boto_error}.\n Error message: {message}')
            return
    except RequestException as err:
        return            

def emoji(active_responce: int):
    if  active_responce == 200:
        emojipic = ':white_check_mark:'
        return emojipic
    elif active_responce != 200:
        emojipic = ':heavy_exclamation_mark:'
        return emojipic
    else:
        emojipic = ':x:'
        return emojipic

def monitior_webserver():
    global active_responce
    global responce_error
    try:
        responce = requests.get(host)
        if responce.status_code == active_responce:
            responce_error = False
        else:
            if responce.status_code != active_responce and responce.status_code == 200:
                responce_error = False
                active_responce = responce.status_code
                emojipic = emoji(active_responce)
                slack_sender(f'Application returned {responce.status_code}.{emojipic}')
            else:
                responce_error = False
                active_responce = responce.status_code
                emojipic = emoji(active_responce)
                logger.info(f'Application returned {responce.status_code}.')
                slack_sender(f'Application returned {responce.status_code}.{emojipic}. Restart docker container...')

                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.connect(host_ip, username='ubuntu', pkey=key_file)
                stdin, stdout, stderr = ssh.exec_command(f'docker restart {container_name}')
                print(stdout.readlines())
                ssh.close
    except RequestException as err:
        if responce_error == True:
            pass      
        else:
            responce_error = True
            slack_sender(f'Requests Error: {err}:x:\nRebooting Web-Server...')
            logger.error(err)
            reboot_webserver()
            return

schedule.every(10).seconds.do(monitior_webserver)

while True:
    schedule.run_pending()


          