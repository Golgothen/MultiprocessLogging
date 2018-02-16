import logging, logging.config
from multiprocessing import Process, Event
from time import sleep


class Worker(Process):
    def __init__(self, name, logConfig):
        super(Worker, self).__init__()
        self.name = name
        self.__stop_event = Event()
        self.config = logConfig
    
    def run(self):
        logging.config.dictConfig(self.config)
        logger = logging.getLogger(__name__)
        while True:
            logger.debug('Process {} logging...'.format(self.name))
            if self.__stop_event.is_set():
                logger.info('Process {} stopping...'.format(self.name))
                break
            sleep(1)
    
    def stop(self):
        self.__stop_event.set()
        
            