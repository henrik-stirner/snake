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


class AuswertungFenster(Nebenfenster):
    def __init__(self, launcher_fenster, spiel) -> None:
        super().__init__(launcher_fenster)
        self.title("Auswertung")

        self.spiel = spiel
    
        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self):
        super().interface_generieren()

        # Score-Label
        self.score_label = Label(self.frame, style="Big.TLabel", text="Score soll hier angezeigt werden.")
        self.score_label.pack()

        # Wiederholen-Knopf
        self.wiederholen_knopf = Button(self.frame, style="Big.TButton", text="ERNEUT SPIELEN", command=self.eingabe)
        self.wiederholen_knopf.pack(fill=X)

        # Beenden-Knopf
        self.beenden_knopf = Button(self.frame, style="Big.TButton", text="BEENDEN", command=self.abbruch)
        self.beenden_knopf.pack(fill=X)

    def eingabe(self):
        self.schliessen()
        self.hauptfenster.spiel_starten()

    def abbruch(self):
        self.schliessen()
