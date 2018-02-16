from mplogger import *
from subprocess import SubProcess
from time import sleep

if __name__ == '__main__':
    #Start the listener
    
    listener = LogListener()
    listener.start()
    
    logging.config.dictConfig(sender_config)
    logger = logging.getLogger('application')
    
    logger.info('Starting subprocesses')
    
    procs = []
    for i in range(5):
        procs.append(SubProcess('SP{}'.format(i)))
        procs[i].start()
    
    #Let the subprocesses run for 10 seconds, then tell them to stop
    sleep(10)
    for p in procs:
        p.stop()
        p.join()
    
    logger.info('Subprocesses stopped')
    listener.stop()
    