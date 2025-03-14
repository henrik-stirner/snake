from configparser import ConfigParser
import logging

from tkinter import BOTH
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

from win.tl.base import Nebenfenster
from win.tl.nameeingabefenster import NameEingabeFenster
from win.tl.pausefenster import PauseFenster
from win.tl.auswertungfenster import AuswertungFenster

from gme.klassisch import KlassischesSpiel
from gme.mehrspieler import MehrspielerSpiel
from gme.wandlos import WandlosSpiel
from gme.computer import ComputerSpiel
from gme.simulation import SimulationSpiel

# ----------


class SpielFenster(Nebenfenster):
    w, h = int(config["Spiel"]["w"]), int(config["Spiel"]["h"])
    eingaben = []

    def __init__(self, launcher_fenster, spielart) -> None:
        super().__init__(launcher_fenster)
        self.title(f"{spielart}")

        self.kacheln = [[None for _ in range(self.h)] for _ in range(self.w)]

        self.spielart = spielart
        self.spiel = None

        # modifizierte Hauptschleife, die auch Spiellogik ausfuehrt
        self.running = True
        self.hauptschleife_id = None

        self.interface_generieren()

        match spielart:
            case "Klassisch":
                NameEingabeFenster(self, 1)
            case "Mehrspieler":
                NameEingabeFenster(self, 2)
            case "Wandlos":
                NameEingabeFenster(self, 1)
            case "Gegen Computer": 
                NameEingabeFenster(self, 1)
            case "Simulation":
                self.spiel_starten(None)


    def spiel_starten(self, namen: list[str] = None):
        match self.spielart:
            case "Klassisch":
                self.spiel = KlassischesSpiel(self, *namen)
            case "Mehrspieler":
                self.spiel = MehrspielerSpiel(self, *namen)
            case "Wandlos":
                self.spiel = WandlosSpiel(self, *namen)
            case "Gegen Computer": 
                self.spiel = ComputerSpiel(self, *namen)
            case "Simulation":
                self.spiel = SimulationSpiel(self)

        self.hauptschleife()

    def taste(self, event):
        taste = event.char

        if taste == "\x1b":  # Escape
            self.running = False
            self.pausieren()
            return

        if taste in self.spiel.erlaubte_eingaben:
            self.eingaben.append(taste)

        logger.debug(f"{taste} {taste in self.spiel.erlaubte_eingaben}")

    def interface_generieren(self):
        super().interface_generieren()
        self.frame.pack(expand=True, fill=BOTH)  # soll sich auch in y-Richtung ausdehnen

        # Spielfeld
        self.spielfeld = Frame(self.frame)
        self.spielfeld.grid_columnconfigure(tuple(range(self.w)), weight=1)  # expand
        self.spielfeld.grid_rowconfigure(tuple(range(self.h)), weight=1)
        self.spielfeld.pack(expand=True, fill=BOTH)

        # Farbe der Labels beim Hovern veraender, sodass man das Raster besser erkennen kann (interaktiver)
        mod = 0x111111  # Unterschied zwischen den Farben

        for x in range(self.w):
            for y in range(self.h):
                kachel = Label(self.spielfeld)
                kachel.grid(column=x, row=y, sticky="NESW")
                self.kacheln[x][y] = kachel

    def _kachel(self, column: int, row: int):
        try:
            # Es gibt nur ein Objekt in der Zelle, und das ist der Frame.
            return self.spielfeld.grid_slaves(column=column, row=row)[0]
        except Exception as e:
            logger.exception(e)

    def kachel_faerben(self, x, y, farbe):
        if not ((0 <= x <= self.w - 1) and (0 <= y <= self.h - 1)):
            logger.warning(f"Kachel ({x}, {y}) liegt außerhalb des Spielfelds")
            return

        # Manchmal gibt es hier Probleme mit persistenten referenzen von Widgets seitens tcl
        # Die entsprechenden Objekte werden womöglich nicht sachgemäß vom Garbage Collector gelöscht?
        try:
            kachel = self.kacheln[x][y]
            if kachel and kachel.winfo_exists():
                kachel.config(background=farbe)
            else:
                logger.warning(f"Kachel ({x}, {y}) existiert nicht mehr.")
        except Exception as e:
            logger.exception(f"self.kacheln : {e}")

    def hauptschleife(self):
        if self.running:
            try:
                self.spiel.aktualisieren()
                self.update()
            except Exception as e:
                logger.error(e)

            # separater Thread, um mainloop nicht zu blockieren
            self.hauptschleife_id = self.after(int(float(self.spiel.delay) * 500), self.hauptschleife)
    
    def pausieren(self):
        PauseFenster(self)

    def schliessen(self):
        self.running = False
        # hauptschleifen (Thread) auslaufen lassen, sodass keine geloeschten Variablen referenziert werden
        self.after(100, self._schliessen)

    def _schliessen(self):
        self.destroy()
        AuswertungFenster(self.hauptfenster, self.spiel)

        # zirkulaere Refenz entfernen
        self.spiel.spiel_fenster = None
        self.spiel = None
        del self.spiel
        del self
