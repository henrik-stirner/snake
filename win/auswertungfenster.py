from typing import *
from configparser import ConfigParser
import logging

from tkinter import *
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


# Neuer Code muss eingefügt werden
'''
from tkinter import *
score = 100
BabaFenster = Tk()
BabaFenster.geometry("1600x900")
BabaFenster.title("AuswertungsFenster")

schlange_frame = Frame(BabaFenster)
schlange_frame.pack(expand=True)

schlange = Frame(schlange_frame, width=500, height=100)
schlange.grid_columnconfigure(tuple(range(5)), weight=1)
schlange.grid_rowconfigure(0, weight=1)
schlange.pack_propagate(0)
schlange.pack()

farbe = 0x2EbA18
for buchstabe in "SNAKE":
    buchstabe_label = Label(schlange, text=buchstabe,
                            fg="white", bg=f"#{hex(farbe).removeprefix('0x')}")
    buchstabe_label.pack(side=LEFT, expand=True, fill=BOTH)
    farbe += 16

ScoreLabel = Label(BabaFenster, text="Score: "+str(score),bg="green")
ScoreLabel.pack(side="top", fill="both",padx="30",pady="40")
ReTryButton = Button(BabaFenster,text="Retry",bg="red")
ReTryButton.pack(side="bottom", fill="both",padx="30",pady="40")
QuitButton = Button(BabaFenster,text="Quit?",bg="green")
QuitButton.pack(side="bottom", fill="both",padx="30",pady="50")
BabaFenster.mainloop()
'''