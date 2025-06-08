"""Dictionary configuration for loggers"""

from logging import (
    getLogger,
    config
)


LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'console': { 
            'format': '\n[%(levelname)s - %(asctime)s] \n %(message)s'
        },
        'file': { 
            'format': '%(levelname)s | %(asctime)s | %(message)s'
        },
    },
    'handlers': { 
        'stream': { 
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
        'general': { 
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'file',
            'filename': 'alm/logs/general.log', 
        },
        'errors': { 
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'file',
            'filename': 'alm/logs/errors.log', 
        },
    },
    'loggers': { 
        'stream': { 
            'handlers': ['stream'],
        },
        'general': { 
            'handlers': ['general'],
        },
        'errors': { 
            'handlers': ['errors'],
        },
    }, 
    'root': {
        'handlers': [],
        'level': 'DEBUG'
    }
}

config.dictConfig(LOGGING_CONFIG)
SLOG = getLogger('stream')
