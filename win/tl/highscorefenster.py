from typing import *
from configparser import ConfigParser
import logging

from tkinter import *


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

# ...

# ----------


class EinstellungFenster(Toplevel):
    def __init__(self, launcher_fenster) -> None:
        super().__init__(launcher_fenster)

        self.focus_force()

        self.launcher_fenster = launcher_fenster

        self.title("Snake: Einstellungen")
        self.configure(background="black")
        # self.minsize(config["Window"]["w"], config["Window"]["h"])
        self.geometry(
            f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}"
        )
    
        self.interface_generieren()

        self.protocol("WM_DELETE_WINDOW", self.schliessen)

        def bei_tastendruck(event):
            taste = event.char

            if taste == "\x1b":  # Escape
                self.schliessen()

        self.bind('<Key>', bei_tastendruck)

        self.mainloop()

    def interface_generieren(self) -> None:
        pass

    def _daten_laden(self):
        pass

    def schliessen(self):
        self.destroy()
