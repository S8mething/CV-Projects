import boto3
import time
import logging
from botocore.exceptions import ClientError
from datetime import datetime
from slack_sender import send_message_to_slack
from slack_sender import aws_alerts_channel_id
from slack_sender import context_ec2_instances
from logging_config import LOGGING_CONFIG


ec2_client_paris = boto3.client('ec2', region_name='eu-west-3')
ec2_client_stockholm = boto3.client('ec2', region_name='eu-north-1')

logger = logging.getLogger('boto_core_logger')
logging.config.dictConfig(LOGGING_CONFIG)

paris_state = 'running'
paris_sys_status = 'ok'
paris_ins_status = 'ok'

def check_instance_paris():
    global paris_state
    global paris_sys_status
    global paris_ins_status
    try:      
        statuses = ec2_client_paris.describe_instance_status(IncludeAllInstances=True)
        for status in statuses['InstanceStatuses']:
            az = status['AvailabilityZone']
            current_ins_status = status['InstanceStatus']['Status']
            current_sys_status = status['SystemStatus']['Status']
            current_state = status['InstanceState']['Name']

            if current_state == paris_state and current_ins_status == paris_ins_status and current_sys_status == paris_sys_status:
                break
            else:
                paris_state = current_state
                paris_sys_status = current_sys_status
                paris_ins_status = current_ins_status
                emojipic = emoji(current_state, current_sys_status, current_ins_status)

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                send_message_to_slack(f'{dt_string} - Instance {status["InstanceId"]} in {az} is {current_state} '
                    f'with instance status is {current_ins_status} '
                    f'and system status is {current_sys_status} {emojipic}', aws_alerts_channel_id, context_ec2_instances)

                logger.info(f'Instance {status["InstanceId"]} in {az} is {current_state} ' 
                            f'Instance status is {current_ins_status} '
                            f'system status is {current_sys_status}')                 
    except ClientError as error:
        send_message_to_slack(f'{error}', aws_alerts_channel_id, context_ec2_instances)
        logger.error(error)

stockholm_state = 'running'
stockholm_sys_status = 'ok'
stockholm_ins_status = 'ok'

def check_instance_stockholm():
    global stockholm_state
    global stockholm_sys_status
    global stockholm_ins_status
    try:      
        statuses = ec2_client_stockholm.describe_instance_status(IncludeAllInstances=True)
        for status in statuses['InstanceStatuses']:
            az = status['AvailabilityZone']
            current_ins_status = status['InstanceStatus']['Status']
            current_sys_status = status['SystemStatus']['Status']
            current_state = status['InstanceState']['Name']

            if current_state == stockholm_state and current_ins_status == stockholm_ins_status and current_sys_status == stockholm_sys_status:
                break
            else:
                stockholm_state = current_state
                stockholm_sys_status = current_sys_status
                stockholm_ins_status = current_ins_status
                emojipic = emoji(current_state, current_sys_status, current_ins_status)

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")            
                send_message_to_slack(f'{dt_string} - Instance {status["InstanceId"]} in {az} is {current_state} '
                                    f'with instance status is {current_ins_status} '
                                    f'and system status is {current_sys_status} {emojipic}', aws_alerts_channel_id, context_ec2_instances)

                logger.info(f'Instance {status["InstanceId"]} in {az} is {current_state} ' 
                            f'Instance status is {current_ins_status} '
                            f'system status is {current_sys_status}')                         
    except ClientError as error:
        send_message_to_slack(f'{error}', aws_alerts_channel_id, context_ec2_instances)
        logger.error(error)

def emoji(state: str, sys_status: str, ins_status: str):
    if  state == 'running' and sys_status == 'ok' and ins_status =='ok':
        emojipic = ':white_check_mark:'
        return emojipic
    elif state == 'running' and sys_status and ins_status != 'ok':
        emojipic = ':heavy_exclamation_mark:'
        return emojipic
    else:
        emojipic = ':x:'
        return emojipic
     
while True:
    check_instance_paris()
    check_instance_stockholm()
    time.sleep(300)









