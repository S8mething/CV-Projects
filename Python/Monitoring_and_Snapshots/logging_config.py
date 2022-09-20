import logging.config


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'slack_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'filename' : 'slack.log',
            'formatter': 'default_formatter'
        },
        'aws_boto_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'filename' : 'aws_boto.log',
            'formatter': 'default_formatter'
        },
    },

    'loggers': {
        'slack_logger': {
            'handlers': ['stream_handler', 'slack_file_handler'],
            'level': 'INFO',
            'propagate': True
        },
        'aws_boto_logger': {
            'handlers': ['stream_handler', 'aws_boto_file_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
