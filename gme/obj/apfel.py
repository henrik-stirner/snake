from typing import *
from configparser import ConfigParser
import logging


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.base import SpielObjekt

# ----------


class Apfel(SpielObjekt):
    def __init__(self, spiel, x, y):
        super().__init__(spiel, x, y, "red")
