from mplogger import *
from multiprocessing import Process, Event
from time import sleep

logging.config.dictConfig(sender_config)
logger = logging.getLogger(__name__)

class SubProcess(Process):
    def __init__(self, name):
        super(SubProcess, self).__init__()
        self.name = name
        self.__stop_event = Event()
    
    def run(self):
        while True:
            logging.info('Process {} logging...'.format(self.name))
            if self.__stop_event.is_set():
                break
            sleep(1)
    
    def stop(self):
        self.__stop_event.set()
        
            