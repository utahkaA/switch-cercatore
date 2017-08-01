from crontab import CronTab
import logging

from switch_cercatore import switch_cercatore
import job

def job1():
    cercatore = switch_cercatore()
    cercatore.start_check()

def _main():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.DEBUG,
                        format=log_fmt,
                        datefmt=date_fmt)
    config = job.config(CronTab("*/2 * * * *"), job1)
    job.controller(config)

if __name__ == "__main__":
    _main()
