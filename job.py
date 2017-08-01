import math
import time
from datetime import datetime, timedelta
import logging
from crontab import CronTab

class config(object):
    def __init__(self, crontab, job):
        """
        """
        self._crontab = crontab
        self.job = job

    def schedule(self):
        crontab = self._crontab
        now = datetime.now()
        delta = timedelta(seconds=math.ceil(crontab.next()))
        return now + delta

    def next(self):
        crontab = self._crontab
        time_to_wait = math.ceil(crontab.next())
        return time_to_wait

def controller(config):
    logging.info("Contorller - Start processing")
    while True:
        try:
            msg = "Contorller - Next schedule: {0}"
            schedule = config.schedule().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(msg.format(schedule))

            time.sleep(config.next())

            logging.info("Contorller - Start job")

            config.job()

            logging.info("Contorller - Finished job")
        except KeyboardInterrupt:
            break
        logging.info("Contorller - Finished processing")
