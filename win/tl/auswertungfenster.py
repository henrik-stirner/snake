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

from gme.obj.schlange import SchlangenKopf

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

        # Datenermittlung (Auswertung)
        schlangen = []
        gewinner = None

        for obj in self.spiel.spielobjekte:
            if not isinstance(obj, SchlangenKopf):
                continue

            schlangen.append(obj)

            if not obj.tot:
                if gewinner is None:
                    gewinner = obj
                elif obj.laenge > gewinner.laenge:
                    gewinner = obj

        schlangen.sort(key=lambda obj: obj.laenge, reverse=True)

        # Anzeige
        self.score_frame = Frame(self.frame)
        self.score_frame.pack(pady=25, padx=25)

        farbe = lambda obj: "red" if obj.tot else "green" if obj.name == gewinner.name else "white"
        for obj in schlangen:
            anzeigetext = f"{obj.laenge} | {obj.name}"

            self.score_label = Label(self.score_frame, foreground=farbe(obj), text=anzeigetext)
            self.score_label.pack(expand=True, fill=X)

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
