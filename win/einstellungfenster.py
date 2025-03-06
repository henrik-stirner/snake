from typing import *
from configparser import ConfigParser
import logging

from tkinter import *
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
    def __init__(self, launcher_fenster, spiel) -> None:
        super().__init__(launcher_fenster)
        self.title("Einstellungen")

        self.spiel = spiel
    
        self.interface_generieren()
        self.mainloop()

    def einstellungen_speichern(self):
        pass
