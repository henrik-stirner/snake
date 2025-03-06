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
from win.pausefenster import PauseFenster
from win.auswertungfenster import AuswertungFenster
from gme.klassisch import KlassischesSpiel
from gme.mehrspieler import MehrspielerSpiel

# ----------


class SpielFenster(Nebenfenster):
    w, h = int(config["Game"]["w"]), int(config["Game"]["h"])
    eingaben = []

    def __init__(self, launcher_fenster, spielart) -> None:
        super().__init__(launcher_fenster)
        self.title(f"{spielart}")

        self.kacheln = [[None for _ in range(self.h)] for _ in range(self.w)]

        self.spiel = None
        match spielart:
            case "Klassisch":
                self.spiel = KlassischesSpiel(self)
            case "Mehrspieler":
                self.spiel = MehrspielerSpiel(self)

        # modifizierte Hauptschleife, die auch Spiellogik ausfuehrt
        self.running = True
        self.hauptschleife_id = None

        self.interface_generieren()
        self.hauptschleife()

    def taste(self, event):
        taste = event.char

        if taste == "\x1b":  # Escape
            self.running = False
            self.pausieren()

        if taste in self.spiel.erlaubte_eingaben:
            self.eingaben.append(taste)

        logger.debug(f"{taste} {taste in self.spiel.erlaubte_eingaben}")

    def interface_generieren(self):
        super().interface_generieren()

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
            logger.error(e)

    def kachel_faerben(self, x, y, farbe):
        try:
            kachel = self.kacheln[x][y]
            if kachel and kachel.winfo_exists():
                kachel.config(background=farbe)
            else:
                logger.warning(f"Kachel ({x}, {y}) existiert nicht mehr.")
        except Exception as e:
            logger.error(f"self.kacheln : {e}")

    def hauptschleife(self):
        if self.running:
            try:
                self.spiel.aktualisieren()
            except Exception as e:
                logger.error(e)

            # separater Thread, um mainloop nicht zu blockieren
            self.hauptschleife_id = self.after(int(float(self.spiel.delay) * 500), self.hauptschleife)
    
    def pausieren(self):
        PauseFenster(self)

    def schliessen(self):
        self.running = False
        # sicherstellen, dass attribute nicht nach dem Schließen noch referenziert werden
        self.after_cancel(self.hauptschleife_id)
        self.after(100, self.tatsaechlich_schliessen)

    def tatsaechlich_schliessen(self):
        if not self.running:
            self.destroy()
            AuswertungFenster(self.hauptfenster, self.spiel)
