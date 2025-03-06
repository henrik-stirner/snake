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

# ----------


class Launcher(Hauptfenster):
    def __init__(self) -> None:
        super().__init__()
        self.title("Launcher")

        self.spiel_fenster = None
        self.spiel = None

        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self) -> None:
        super().interface_generieren()

        # Schlange
        self.schlange_frame = Frame(self.frame)
        self.schlange_frame.pack(expand=True)

        self.schlange = Frame(self.schlange_frame, width=500, height=100)
        self.schlange.grid_columnconfigure(tuple(range(5)), weight=1)
        self.schlange.grid_rowconfigure(0, weight=1)
        self.schlange.pack_propagate(0)
        self.schlange.pack()

        farbe = 0x2EbA18
        for buchstabe in "SNAKE":
            hex_code = f"#{hex(farbe).removeprefix('0x')}"

            stil = Style()
            stil.configure("Custom.TFrame", background=hex_code)

            buchstabe_frame = Frame(self.schlange, style="Custom.TFrame")
            buchstabe_frame.pack(side=LEFT, expand=True, fill=BOTH)

            buchstabe_label = Label(buchstabe_frame, text=buchstabe, background=hex_code)
            buchstabe_label.pack(expand=True)

            farbe += 16

        # Startknopf
        self.start_knopf = Button(self.frame, style="Big.TButton", command=self._on_start, text="STARTEN")
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

    def _on_start(self):
        self.withdraw()  # Launcher verstecken
        SpielFenster(self, self.modus_dropdown.get())
