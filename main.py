from configparser import ConfigParser
import logging.config
from os import walk, remove, system
from datetime import datetime

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


# only keep up to 5 log files
logfiles = list(filter(
    lambda file: file.endswith('.log') or file.split('.')[-1].isdigit(),
    next(walk('log/'), (None, None, []))[2]
))
if len(logfiles) > 5:
    for logfile in logfiles[0:len(logfiles) - 5]:
        remove(f'log/{logfile}')
del logfiles


logging.config.fileConfig(
            './logger.ini',
            encoding='utf-8',
            defaults={
                'logfilename':
                    f'./log/{datetime.now().strftime("%Y-%m-%d_-_%H-%M-%S")}.log'
            }
        )
logger = logging.getLogger(__name__)


# ----------
# eigene imports
# ----------


from win.launcher import Launcher


# ----------
# main
# ----------


script = __file__


def main():
    launcher = Launcher()
    while launcher.running:
        launcher.update()

    if launcher.wiederholen:
        del launcher
        system(f"python {script}")


if __name__ == "__main__": 
    main()
