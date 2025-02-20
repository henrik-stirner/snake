from typing import *
from configparser import ConfigParser
import logging
from logging.config import fileConfig
from os import walk, remove
from datetime import datetime


from win.launcher import Launcher


# ----------
# config
# ----------


config = ConfigParser()
config.read("./config.ini")


# ----------
# logging
# ----------


"""
----------
USAGE
----------
display output for ordinary cli:
    print()
report events (status monitoring, fault investigation):
    logger.info() or
    logger.debug() for detailed output
issue warnings (particular runtime events):
    issue is avoidable and the code should be modified:
        warnings.warn()
    the event should be noticed, but there is nothing you can do about it:
        logger.warning()
report errors (particular runtime events):
    catch Error/
    raise MostSpecificError()
report suppressed errors without raising exceptions:
    logger.error() or
    logger.exception() or
    logger.critical()
----------
"""


logging.config.fileConfig(
            './logger.ini',
            encoding='utf-8',
            defaults={
                'logfilename':
                    f'./log/{datetime.now().strftime("%Y-%m-%d_-_%H-%M-%S")}.log'
            }
        )
logger = logging.getLogger(__name__)

# only keep up to 5 log files
logfiles = list(filter(
    lambda file: file.endswith('.log') or file.split('.')[-1].isdigit(),
    next(walk('log/'), (None, None, []))[2]
))
if len(logfiles) > 5:
    for logfile in logfiles[0:len(logfiles) - 5]:
        remove(f'log/{logfile}')
del logfiles


# ----------
# game
# ----------


def main(): 
    Launcher()


if __name__ == "__main__": 
    main()
