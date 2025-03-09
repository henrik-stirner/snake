from configparser import ConfigParser
import logging
from os.path import abspath

from tkinter import PhotoImage, LEFT, RIGHT, X, Y, BOTH
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

from win.base import Hauptfenster
from win.tl.scorefenster import ScoreFenster
from win.tl.einstellungfenster import EinstellungFenster
from win.tl.spielfenster import SpielFenster

# ----------


class Launcher(Hauptfenster):
    def __init__(self) -> None:
        super().__init__()
        self.title("Launcher")

        self.running = True
        self.wiederholen = False

        self.interface_generieren()

    def interface_generieren(self) -> None:
        super().interface_generieren()
        self.frame.pack(expand=True, fill=BOTH)  # soll sich auch in y-Richtung ausdehnen

        # Score- und Einstellungsknopf
        self.menue_frame = Frame(self.frame)
        self.menue_frame.pack(fill=X)

        self.pokal_pi = PhotoImage(file=abspath("./ico/pokal.png"))
        self.score_knopf = Button(self.menue_frame, style="Ico.TButton", image=self.pokal_pi, command=self.scores_anzeigen)
        self.score_knopf.pack(side=LEFT)

        self.zahnrad_pi = PhotoImage(file=abspath("./ico/zahnrad.png"))
        self.einstellung_knopf = Button(self.menue_frame, style="Ico.TButton", image=self.zahnrad_pi, command=self.einstellungen_anzeigen)
        self.einstellung_knopf.pack(side=RIGHT)

        # Schlange
        self.schlange_frame = Frame(self.frame)
        self.schlange_frame.pack(expand=True)

        self.schlange = Frame(self.schlange_frame)
        self.schlange.grid_columnconfigure(tuple(range(5)), weight=1)
        self.schlange.grid_rowconfigure(0, weight=1)
        self.schlange.pack()

        text, farben = "A SNAKE", ["red", "black", "darkgreen", "green", "green", "green", "green"]

        # oder Farbverlauf generieren:
        # farbe, mod = 0x2EbA18, 0x000016
        # farben = [f"#{hex(farbe + i * mod).removeprefix('0x')}" for i in range(len(text))]

        for i, buchstabe in zip(range(len(text)), text):
            buchstabe_label = Label(self.schlange, text=buchstabe, background=farben[i], padding=(25, 20))
            buchstabe_label.grid(row=0, column=i, sticky="NEWS")

        # Startknopf
        self.start_knopf = Button(self.frame, style="Big.TButton", command=self.spiel_starten, text="STARTEN")
        self.start_knopf.pack(fill=X)

        # Modus-Dropdown
        self.modus_dropdown = Combobox(self.frame,
            state="readonly",
            values=["Klassisch", "Mehrspieler", "Gegen Computer"]
        )
        self.modus_dropdown.current(int(config["Spiel"]["mode"]))
        self.modus_dropdown.pack(pady=10)

        # Ranking
        self.ranking_frame = Frame(self.frame)
        self.ranking_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        self.ranking_frame.pack(expand=True)

        self.spieler_frame = Frame(self.ranking_frame)
        self.spieler_frame.grid(row=0, column=0, sticky="news")

        self.score_frame = Frame(self.ranking_frame)
        self.score_frame.grid(row=0, column=1, sticky="news")

        with open("scores.txt", "r") as lesedatei:
            scores = [zeile for zeile in lesedatei.readlines() if (zeile.strip())]
            scores.sort(key=lambda x: int(x.split()[1]), reverse=True)

            for highscore in scores[:5]:
                spieler, score = highscore.split()

                spieler_label = Label(self.spieler_frame, text=spieler)
                spieler_label.pack(expand=True, fill=X)
                score_label = Label(self.score_frame, text=score)
                score_label.pack(expand=True, fill=X)

    def spiel_starten(self):
        self.withdraw()  # Launcher verstecken
        SpielFenster(self, self.modus_dropdown.get())

    def scores_anzeigen(self):
        self.withdraw()
        ScoreFenster(self)

    def einstellungen_anzeigen(self):
        self.withdraw()
        EinstellungFenster(self)

    def eingabe(self):
        self.spiel_starten()

    def einstellungen_speichern(self):
        # gewaehlten Modus speichern
        config.set("Spiel", "mode", str(self.modus_dropdown.current()))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def schliessen(self):
        self.running = False
        self.destroy()
