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
        self.anzeige_frame = Frame(self.frame)
        self.anzeige_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        self.anzeige_frame.pack(pady=25, padx=25)

        self.spieler_frame = Frame(self.anzeige_frame)
        self.spieler_frame.grid(row=0, column=0, sticky="news")
        self.spieler_info_label = Label(self.spieler_frame, text="SPIELER")
        self.spieler_info_label.pack(expand=True, fill=X, pady=10)

        self.score_frame = Frame(self.anzeige_frame)
        self.score_frame.grid(row=0, column=1, sticky="news")
        self.score_info_label = Label(self.score_frame, text="SCORE")
        self.score_info_label.pack(expand=True, fill=X, pady=10)

        farbe = lambda obj: "red" if obj.tot else "green" if obj.name == gewinner.name else "white"
        for obj in schlangen:
            spieler_label = Label(self.spieler_frame, foreground=farbe(obj), text=obj.name)
            spieler_label.pack(expand=True, fill=X)
            score_label = Label(self.score_frame, foreground=farbe(obj), text=str(obj.laenge))
            score_label.pack(expand=True, fill=X)

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
