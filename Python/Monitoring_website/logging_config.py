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
        'monitoring_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'filename' : 'website.log',
            'formatter': 'default_formatter'
        },
    },

    'loggers': {
        'slack_logger': {
            'handlers': ['stream_handler', 'slack_file_handler'],
            'level': 'INFO',
            'propagate': True
        },
        'monitoring_logger': {
            'handlers': ['stream_handler', 'monitoring_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
