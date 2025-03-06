from typing import *
from configparser import ConfigParser
import logging

from tkinter import X, Y, LEFT, RIGHT, TOP, BOTTOM, BOTH
from tkinter.ttk import *


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from win.base import Nebenfenster

# ----------


class EinstellungFenster(Nebenfenster):
    def __init__(self, launcher_fenster) -> None:
        super().__init__(launcher_fenster)
        self.title("Highscores")
    
        self.interface_generieren()
        self.mainloop()

    def _daten_laden(self):
        pass
