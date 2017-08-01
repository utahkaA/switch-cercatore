import os
import os.path
from crontab import CronTab
import logging
import logging.handlers as handlers

from switch_cercatore import switch_cercatore
import job

def job1():
    cercatore = switch_cercatore()
    cercatore.start_check()

def _main():
    if not os.path.exists("./log"):
        os.mkdir("./log")

    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.DEBUG,
                        format=log_fmt,
                        datefmt=date_fmt)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = handlers.TimedRotatingFileHandler(
            filename='log/cercatore.log',
            when='H',
            interval=1,
            backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(log_fmt))
    logger.addHandler(file_handler)

    config = job.config(CronTab("*/2 * * * *"), job1)
    job.controller(config)

if __name__ == "__main__":
    _main()
