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

# ...

# ----------


class AuswertungFenster(Toplevel):
    def __init__(self, launcher_fenster, spiel) -> None:
        super().__init__(launcher_fenster)

        self.focus_force()

        self.launcher_fenster = launcher_fenster

        self.spiel = spiel

        self.title("Snake: Klassisches Spiel")
        self.configure(background="black")
        # self.minsize(config["Window"]["w"], config["Window"]["h"])
        self.geometry(
            f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}"
        )
    
        self.interface_generieren()

        self.protocol("WM_DELETE_WINDOW", self.schliessen)

        def bei_tastendruck(event):
            taste = event.char

            if taste == "\x1b":  # Escape
                self.schliessen()

        self.bind('<Key>', bei_tastendruck)
        self.bind('<Return>', lambda args: self._on_start())

        self.mainloop()

    def interface_generieren(self) -> None:
        pass
        
    def _score_speichern():
        pass

    def schliessen(self):
        self._score_speichern
        self.destroy()
        self.launcher_fenster.deiconify()
        self.launcher_fenster.start_knopf.config(state="normal")

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