from configparser import ConfigParser
import logging

from tkinter import X
from tkinter.ttk import *


# ----------
# config und logger
# ----------

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
        self.schlangen = []

        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self):
        super().interface_generieren()

        # Datenermittlung (Auswertung)
        gewinner = []

        for obj in self.spiel.spielobjekte:
            if not isinstance(obj, SchlangenKopf):
                continue

            self.schlangen.append(obj)

            if not gewinner:
                # extra if-clause, da liste mit Laenge groesser 1 fuer weitere Bedingungen vorausgesetzt
                gewinner = [obj]
            elif ((obj.laenge > gewinner[0].laenge) or
                  (obj.laenge == gewinner[0].laenge and gewinner[0].tot and not obj.tot)
            ):
                gewinner = [obj]
            elif obj.laenge == gewinner[0].laenge and obj.tot == gewinner[0].tot:
                gewinner.append(obj)

        self.schlangen.sort(key=lambda obj: obj.laenge, reverse=True)

        # Anzeige
        self.gewinner_label = Label(
            self.frame, style="Big.TLabel",
            text=f"{', '.join([schlange.name for schlange in gewinner])} {'haben' if len(gewinner) > 1 else 'hat'} das Spiel gewonnen!")
        self.gewinner_label.pack()

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

        gewinner_namen = [obj.name for obj in gewinner]
        farbe = lambda obj: "red" if obj.tot else "green" if obj.name in gewinner_namen else "white"
        for obj in self.schlangen:
            spieler_label = Label(self.spieler_frame, foreground=farbe(obj), text=obj.name)
            spieler_label.pack(expand=True, fill=X)
            score_label = Label(self.score_frame, foreground=farbe(obj), text=str(obj.laenge))
            score_label.pack(expand=True, fill=X)

        # Wiederholen-Knopf
        self.zurueck_knopf = Button(self.frame, style="Big.TButton", text="ZURÜCK", command=self.eingabe)
        self.zurueck_knopf.pack(fill=X)

        # Beenden-Knopf
        self.beenden_knopf = Button(self.frame, style="Big.TButton", text="BEENDEN", command=self.abbruch)
        self.beenden_knopf.pack(fill=X)

    def eingabe(self):
        self.schliessen()
        self.hauptfenster.wiederholen = True
        self.hauptfenster.running = False
        self.hauptfenster.schliessen()

    def abbruch(self):
        self.schliessen()
        self.hauptfenster.running = False
        self.hauptfenster.schliessen()

    def score_speichern(self):
        with open("scores.txt", "a") as f:
            f.writelines([f"\n{obj.name}\t{obj.laenge}" for obj in self.schlangen])

    def schliessen(self):
        self.score_speichern()

        super().schliessen()
