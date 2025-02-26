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

from win.launcher import Launcher

# ----------


class AuswertungFenster(Toplevel):
    def __init__(self, launcher_fenster, spiel) -> None:
        super().__init__(launcher_fenster)

        self.focus_force()

        self.launcher_fenster = launcher_fenster

        self.spiel = spiel

        self.title("Snake: Klassisches Spiel")
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
            else:
                self._on_start()

        self.bind('<Key>', bei_tastendruck)

        self.mainloop()

    def interface_generieren(self) -> None:
        pass
        
    def _score_speichern():
        pass

    def schliessen(self):
        self._score_speichern
        self.destroy()
        self.launcher_fenster.deiconify()
        self.launcher_fenster.start_knopf.config(state="normal")
        