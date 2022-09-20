import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from logging_config import LOGGING_CONFIG


client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('slack_logger')

aws_alerts_channel_id = "<id>"
aws_notification_channel_id = "<id>"

context_snapshot = 'AWS Snapshot'
context_ec2_instances = 'AWS EC2 Instances'

def send_message_to_slack(notification_text: str, channel_id, context):
    try:
        result = client.chat_postMessage(
            channel = channel_id,
            text = notification_text,
            blocks = [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": context,
                            "emoji": True
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": notification_text,
                        "emoji": True
                    }
                }
            ]
        )
        status = result["ok"]
        message = result["message"]["text"]
        logger.info(f'Message sent: {status}, text - {message}')
    except SlackApiError as e:
        logger.error(f"Error: {e}")

