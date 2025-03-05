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


class PauseFenster(Toplevel):
    def __init__(self, spiel_fenster) -> None:
        super().__init__(spiel_fenster)

        self.focus_force()

        self.spiel_fenster = spiel_fenster

        self.title("Snake: Pause")
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
                self.beenden()

        self.bind('<Key>', bei_tastendruck)
        self.bind('<Return>', lambda args: self.fortfahren())

        self.mainloop()

    def interface_generieren(self) -> None:
        pass
    
    def fortfahren(self): 
        self.schliessen()
        self.spiel_fenster.running = True
        self.spiel_fenster.hauptschleife()

    def beenden(self):
        self.schliessen()
        self.spiel_fenster.schliessen()
    
    def schliessen(self):
        self.destroy()

