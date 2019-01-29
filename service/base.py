from os import getenv

DATABASE = {
    'default': {
        'drivername': getenv('APP_DATABASES_DEFAULT_ENGINE', 'sqlite'),
        'database': getenv('APP_DATABASES_DEFAULT_NAME', 'dbdata/db.sqlite3')
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'simple': {
            'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

VK_TOKEN = getenv('VK_TOKEN') or 'some token in case no other found'
