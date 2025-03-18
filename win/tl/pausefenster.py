import logging

from tkinter import X
from tkinter.ttk import *


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from win.tl.base import Nebenfenster

# ----------


class PauseFenster(Nebenfenster):
    """
    Fenster, das angezeigt wird, wenn das Spiel pausiert wird.
    """

    def __init__(self, spiel_fenster: object) -> None:
        """
        Initialisierung des Fensters.

        :param spiel_fenster:
        """

        super().__init__(spiel_fenster)
        self.title("Pause")

        self.hauptfenster.running = False
    
        self.interface_generieren()
        self.mainloop()

    def interface_generieren(self) -> None:
        """
        Generiert das Interface des Fensters.

        :return:
        """

        super().interface_generieren()

        # Fortfahren-Knopf
        self.fortfahren_knopf = Button(self.frame, style="Big.TButton", text="FORTFAHREN", command=self.eingabe)
        self.fortfahren_knopf.pack(fill=X)
        # Beenden-Knopf
        self.beenden_knopf = Button(self.frame, style="Big.TButton", text="BEENDEN", command=self.abbruch)
        self.beenden_knopf.pack(fill=X)
    
    def eingabe(self) -> None:
        """
        Wird aufgerufen, wenn der Fortfahren-Knopf oder die Enter-Taste gedrückt wird.

        :return:
        """

        self.schliessen()
        self.hauptfenster.running = True
        self.hauptfenster.hauptschleife()

    def abbruch(self) -> None:
        """
        Wird aufgerufen, wenn der Beenden-Knopf oder die Escape-Taste gedrückt wird.
        In diesem Fall soll auch das Spiel beendet, also das Hauptfenster geschlossen werden.

        :return:
        """

        self.schliessen()
        self.hauptfenster.schliessen()
