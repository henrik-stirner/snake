from configparser import ConfigParser
import logging

from tkinter import X, BOTH
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
        self.ranking_frame.pack(expand=True)

        with open("scores.txt", "r") as lesedatei:
            highscores = [(int(zeile.split()[0]), zeile) for zeile in lesedatei.readlines()]
            highscores.sort(key=lambda x: x[0], reverse=True)

            for highscore in highscores[:5]:
                score_label = Label(self.ranking_frame, text=highscore[1])
                score_label.pack()

    def spiel_starten(self):
        self.withdraw()  # Launcher verstecken
        SpielFenster(self, self.modus_dropdown.get())

    def eingabe(self):
        self.spiel_starten()

    def einstellungen_speichern(self):
        # gewaehlten Modus speichern
        config.set("Spiel", "mode", str(self.modus_dropdown.current()))
        with open("config.ini", "w") as configfile:
            config.write(configfile)
