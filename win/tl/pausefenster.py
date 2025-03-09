from configparser import ConfigParser
import logging

from tkinter import X
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

from win.tl.base import Nebenfenster


# ----------


class PauseFenster(Nebenfenster):
    def __init__(self, spiel_fenster) -> None:
        super().__init__(spiel_fenster)
        self.title("Pause")

        self.hauptfenster.running = False
    
        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self):
        super().interface_generieren()

        # Fortfahren-Knopf
        self.fortfahren_knopf = Button(self.frame, style="Big.TButton", text="FORTFAHREN", command=self.eingabe)
        self.fortfahren_knopf.pack(fill=X)
        # Beenden-Knopf
        self.beenden_knopf = Button(self.frame, style="Big.TButton", text="BEENDEN", command=self.abbruch)
        self.beenden_knopf.pack(fill=X)
    
    def eingabe(self):
        self.schliessen()
        self.hauptfenster.running = True
        self.hauptfenster.hauptschleife()

    def abbruch(self):
        self.schliessen()
        self.hauptfenster.schliessen()
