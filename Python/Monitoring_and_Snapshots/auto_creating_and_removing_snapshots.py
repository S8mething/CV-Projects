import boto3
import schedule
import time
import logging
from botocore.exceptions import ClientError
from operator import itemgetter
from logging_config import LOGGING_CONFIG
from slack_sender import send_message_to_slack
from slack_sender import aws_alerts_channel_id
from slack_sender import aws_notification_channel_id
from slack_sender import context_snapshot

ec2_client_stockholm = boto3.client('ec2', region_name='eu-north-1')
ec2_client_paris = boto3.client('ec2', region_name='eu-west-3')

logger = logging.getLogger('aws_boto_logger')
logging.config.dictConfig(LOGGING_CONFIG)

def create_volume_snapshots(region):
    try:
        reservations = region.describe_instances()
        for instance in reservations['Reservations']:      
            for instance_list in instance['Instances']:
                instance_id = instance_list['InstanceId']
            for ebs_list in instance_list['BlockDeviceMappings']:
                ebs = ebs_list['Ebs']['VolumeId']
                new_snapshot = region.create_snapshot(
                    Description = f'Snapshot of instance {instance_id}',
                    VolumeId = ebs,
                    TagSpecifications =[
                    {
                        'ResourceType': 'snapshot',
                        'Tags': [
                            {
                                'Key': 'Instance',
                                'Value': instance_id
                            },
                        ]
                    },
                ]
            )         
                for attempts in range(5):
                    snapshots = region.describe_snapshots(SnapshotIds=[new_snapshot['SnapshotId']])
                    for snapshot in snapshots['Snapshots']:
                        snapshot_id = new_snapshot['SnapshotId']
                        state = snapshot['State'] 
                    if state == "completed":
                        send_message_to_slack(f'Snapshot successfully created:white_check_mark: Instance {instance_id} - {snapshot_id} in {state} state', aws_notification_channel_id, context_snapshot)
                        logger.info(f'Snapshot successfully created. Instance {instance_id} - Snapshot {snapshot_id}')
                        break  
                    else:
                        if attempts == 5:
                            send_message_to_slack(f'Snapshot failure:x: Instance {instance_id} - {snapshot_id} in {state} state', aws_alerts_channel_id, context_snapshot)
                            logger.error(f'Snapshot failure. Instance {instance_id} - {snapshot_id} in {state} state')
                            break
                        else:
                            time.sleep(15)
    except ClientError as error:
        send_message_to_slack(f'{error}', aws_alerts_channel_id, context_snapshot)
        logger.error(error)                                     

def delete_volume_snapshots(region):
    try:
        volumes = region.describe_volumes()
        for volume in volumes['Volumes']:
            snapshots = region.describe_snapshots(
                OwnerIds=['self'],
                Filters=[
                    {
                        'Name': 'volume-id',
                        'Values': [volume['VolumeId']]
                    }
                ]
            )  
            sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)          
            for snap in sorted_by_date[2:]:
                delete = region.delete_snapshot(
                    SnapshotId=snap['SnapshotId']
                )
                send_message_to_slack(f'Snapshot-{snap["SnapshotId"]}-deleted:heavy_exclamation_mark:', aws_notification_channel_id, context_snapshot)
        time.sleep(10)
    except ClientError as error:
        send_message_to_slack(f'{error}', aws_alerts_channel_id, context_snapshot)
        logger.error(error)                             

schedule.every().day.at("22:30").do(create_volume_snapshots, ec2_client_stockholm)
schedule.every().day.at("22:50").do(create_volume_snapshots, ec2_client_paris)

schedule.every().day.at("23:30").do(delete_volume_snapshots, ec2_client_stockholm)
schedule.every().day.at("23:50").do(delete_volume_snapshots, ec2_client_paris)

while True:
    schedule.run_pending()
    time.sleep(55)

