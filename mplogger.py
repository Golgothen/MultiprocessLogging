from multiprocessing import Process, Event, Queue, current_process
import logging.handlers, logging.config
from datetime import datetime

shared_logging_queue = Queue()

sender_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'queue': {
            'class': 'logging.handlers.QueueHandler',
            'queue': shared_logging_queue,
        },
    },
    'loggers': {
        'application': {
            'level':       'DEBUG',
        },
        'subprocess': {
            'level':       'DEBUG',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['queue']
    },
}

listener_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'respect_handler_level': True,
    'formatters': {
        'detailed': {
            'class':       'logging.Formatter',
            'format':      '%(asctime)-16s:%(name)-21s:%(levelname)-8s[%(module)-13s.%(funcName)-20s %(lineno)-5s] %(message)s'
            },
        'brief': {
            'class':       'logging.Formatter',
            'format':      '%(asctime)-16s:%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class':       'logging.StreamHandler',
            'level':       'ERROR',
            'formatter':   'brief'
        },
        'file': {
            'class':       'logging.FileHandler',
            'filename':    (datetime.now().strftime('RUN-%Y%m%d')+'.log'),
            'mode':        'w',
            'formatter':   'detailed',
        },
        #'filerotate': {
        #    'class':       'logging.handlers.TimedRotatingFileHandler',
        #    'filename':    'run.log',
        #    'when':        'midnight',
        #    'interval':    1,
        #    'formatter':   'detailed',
        #    'backupCount': 10
        #}
    },
    'root': {
        'handlers':    ['console', 'file'],
    },
}


class MyHandler(object):
    def handle(self, record):
        logger = logging.getLogger(record.name)
        record.processName = '%s (for %s)' % (current_process().name, record.processName)
        logger.handle(record)

class LogListener(Process):
    def __init__(self, q):
        super(LogListener, self).__init__()
        self.__stop_event = Event()
        self.name = 'listener'
        self.logQueue = q

    def run(self):
        logging.config.dictConfig(listener_config)
        logger = logging.getLogger('listener')
        logger.info('Logging system initialised')
        listener = logging.handlers.QueueListener(self.logQueue, MyHandler())
        listener.start()
        logger.info('Logging system running')
        while True:
            try:
                self.__stop_event.wait()
                listener.stop()
                logger.info('Logging system stopped')
                break
            except (KeyboardInterrupt, SystemExit):
                listener.stop()
                break
                logger.info('Logging system stopped')

    def stop(self):
        self.__stop_event.set()
