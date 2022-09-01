import logging
import logging.config
import sys

class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        """Only lets through log messages with log level below ERROR (numeric value: 40)."""
        return record.levelno < 50
    
config = {
    'version': 1,
    'filters': {
        'exclude_errors': {
            '()': _ExcludeErrorsFilter
        }
    },
    'formatters': {
        # Modify log message format here or replace with your custom formatter class
        # Add (%(process)d) to the beginning of the format to get the process id
        'log_formatter': {
            'format': '%(levelname)s | %(asctime)s | %(module)s (line %(lineno)s) | %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers': {
        'console_stderr': {
            # Sends log messages with log level ERROR or higher to stderr
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'log_formatter',
            'stream': sys.stderr
        },
        'console_stdout': {
            # Sends log messages with log level higher than INFO to stdout
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'log_formatter',
            'filters': ['exclude_errors'],
            'stream': sys.stdout
        },
        'file': {
            # Sends all log messages to a file with log level higher than INFO
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'log_formatter',
            'filename': 'logs.log',
            'encoding': 'utf8'
        }
    },
    'root': {
        # In general, this should be kept at 'NOTSET'.
        # Otherwise it would interfere with the log levels set for each handler.
        'level': 'NOTSET',
        'handlers': ['console_stderr', 'console_stdout', 'file']
    },
}
    
logging.config.dictConfig(config)
logger = logging.getLogger((__name__))