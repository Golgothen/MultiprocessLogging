from mplogger import *
import logging, logging.config
from worker import Worker
from time import sleep

if __name__ == '__main__':
    #Start the listener
    logQueue = Queue()
    print('Main logQueue {}'.format(logQueue))
    listener = LogListener(logQueue)
    listener.start()
    config = sender_config
    config['handlers']['queue']['queue'] = logQueue
    logging.config.dictConfig(config)
    logger = logging.getLogger('application')
    
    logger.info('Starting subprocesses')
    
    procs = []
    for i in range(5):
        p = Worker('SP{}'.format(i),config)
        procs.append(p)
        p.start()
    
    #Let the subprocesses run for 10 seconds, then tell them to stop
    sleep(10)
    for p in procs:
        p.stop()
        p.join()
    
    logger.info('Subprocesses stopped')
    listener.stop()
    