from configparser import ConfigParser
import logging

from tkinter import X, Y, LEFT, RIGHT, TOP, BOTTOM, BOTH, CENTER
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
from win.spielfenster import SpielFenster

from util import schlange

# ----------


class Launcher(Hauptfenster):
    def __init__(self) -> None:
        super().__init__()
        self.title("Launcher")

        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self) -> None:
        super().interface_generieren()
        self.frame.pack(expand=True, fill=BOTH)  # soll sich auch in y-Richtung ausdehnen

        # Schlange
        self.snake_frame = Frame(self.frame)
        self.snake_frame.pack(expand=True)

        schlange(self.snake_frame, "SNAKE")

        # Startknopf
        self.start_knopf = Button(self.frame, style="Big.TButton", command=self.spiel_starten, text="STARTEN")
        self.start_knopf.pack(fill=X)

        # Modus-Dropdown
        self.modus_dropdown = Combobox(self.frame,
            state="readonly",
            values=["Klassisch", "Mehrspieler", "Gegen Computer"]
        )
        self.modus_dropdown.current(int(config["Game"]["mode"]))
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

    def einstellungen_speichern(self):
        # gewaehlten Modus speichern
        config.set("Game", "mode", str(self.modus_dropdown.current()))
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def spiel_starten(self):
        self.withdraw()  # Launcher verstecken
        SpielFenster(self, self.modus_dropdown.get())
