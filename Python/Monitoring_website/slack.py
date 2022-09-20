import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from logging_config import LOGGING_CONFIG


client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('slack_logger')

website_channel_id = "C042SKZ1UMA"

def slack_sender(notification_text: str):
    try:
        result = client.chat_postMessage(
            channel = website_channel_id,
            text = notification_text,
            blocks = [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": 'Website Status',
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

