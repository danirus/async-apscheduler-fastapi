from pathlib import Path

# Base root directory (parent of application dir).
BASE_PATH = Path(__file__).parents[1]

# The directory path containing the root __init__.py of the package.
DATA_PATH = BASE_PATH / "data"

# Path to the directory from where to read the incoming files.
INBOX_PATH = DATA_PATH / "inbox"

# Path to the directory where to put the processed files.
PROCESSED_PATH = DATA_PATH / "processed"

# Logging configuration.
LOGGING = {
'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'console': {
            'format': ('[%(asctime)s][%(levelname)s] %(name)s '
                       '%(filename)s:%(funcName)s:%(lineno)d | %(message)s'),
            'datefmt': '%H:%M:%S',
        }
    },
    'handlers': {
        'simple': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['simple', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
