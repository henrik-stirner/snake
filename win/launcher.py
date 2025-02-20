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

from win.tl.spielfenster import SpielFenster

# ----------


class Launcher(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.focus_force()

        self.spiel_fenster = None

        self.title("Launcher")
        self.configure(background="black")
        # root.minsize(config["Window"]["w"], config["Window"]["h"])
        self.geometry(
            f"{config['Window']['w']}x{config['Window']['h']}+{config['Window']['x']}+{config['Window']['y']}"
        )

        self.interface_generieren()

        self.mainloop()

    def interface_generieren(self) -> None:
        # Schlange

        self.schlange_frame = Frame(self)
        self.schlange_frame.pack(expand=True)

        self.schlange = Frame(self.schlange_frame, width=500, height=100)
        self.schlange.grid_columnconfigure(tuple(range(5)), weight=1)
        self.schlange.grid_rowconfigure(0, weight=1)
        self.schlange.pack_propagate(0)
        self.schlange.pack()

        farbe = 0x2EbA18
        for buchstabe in "SNAKE":
            buchstabe_label = Label(self.schlange, text=buchstabe, font=config["Font"]["text"],
                                    fg="white", bg=f"#{hex(farbe).removeprefix('0x')}")
            buchstabe_label.pack(side=LEFT, expand=True, fill=BOTH)
            farbe += 16

        # Startknopf

        self.start_knopf = Button(self, command=self._on_start,
                                  text="START", font=config["Font"]["huge"], height=5,
                                  bg="black", fg="white", activeforeground="black", activebackground="white",
                                  highlightthickness=0, bd=0)
        self.start_knopf.pack(fill=X)

        # Ranking

        self.ranking_frame = Frame(self, bg="black")
        self.ranking_frame.pack(expand=True)

        with open("scores.txt", "r") as lesedatei:
            highscores = [(int(zeile.split()[0]), zeile) for zeile in lesedatei.readlines()]
            highscores.sort(key=lambda x: x[0], reverse=True)

            for highscore in highscores[:5]:
                score_label = Label(self.ranking_frame, text=highscore[1], font=config["Font"]["head"],
                                    fg="white", bg="black")
                score_label.pack(expand=True, fill=BOTH)

    def _on_start(self):
        self.withdraw()  # launcher_fenster verstecken
        SpielFenster(self)
