from configparser import ConfigParser
import logging

from tkinter import X, LEFT, RIGHT, CENTER, BOTH, E, W
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

from win.element.frame import VerticalScrolledFrame
from win.tl.base import Nebenfenster

# ----------


class ScoreFenster(Nebenfenster):
    def __init__(self, launcher_fenster) -> None:
        super().__init__(launcher_fenster)
        self.title("Highscores")
    
        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self):
        super().interface_generieren()
        self.frame.pack(expand=True, fill=BOTH)  # soll sich auch in y-Richtung ausdehnen

        # Info-Label
        self.info_label = Label(self.frame, text="SCORES")
        self.info_label.pack(pady=20)

        # Ranking
        self.ranking_frame = VerticalScrolledFrame(self.frame)
        self.ranking_frame.pack(expand=True, fill=BOTH)

        self.spieler_frame = Frame(self.ranking_frame.interior)
        self.spieler_frame.pack(side=LEFT, expand=True, fill=BOTH)

        self.score_frame = Frame(self.ranking_frame.interior)
        self.score_frame.pack(side=RIGHT, expand=True, fill=BOTH)

        with open("scores.txt", "r", encoding="utf-8") as lesedatei:
            scores = [zeile for zeile in lesedatei.readlines() if (zeile.strip())]
            scores.sort(key=lambda x: int(x.split()[1]), reverse=True)

            for zeile in scores:
                spieler, score = zeile.split()

                spieler_label = Label(self.spieler_frame, text=spieler)
                spieler_label.pack(anchor=E)
                score_label = Label(self.score_frame, text=score)
                score_label.pack(anchor=W)
