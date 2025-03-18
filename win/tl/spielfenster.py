import logging

from tkinter import BOTH, Event
from tkinter.ttk import *

# ----------
# logger
# ----------

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
    """
    Fenster, in dem das Spiel stattfindet. (Spielfeld)
    """

    def __init__(self, launcher_fenster: object, spielart: str) -> None:
        """
        Initialisiert das SpielFenster.

        :param launcher_fenster:
        :param spielart:
        """

        super().__init__(launcher_fenster)
        self.title(f"{spielart}")

        self.w, self.h = int(self.config["Spiel"]["w"]), int(self.config["Spiel"]["h"])
        self.eingaben = []

        self.kacheln = [[None for _ in range(self.h)] for _ in range(self.w)]

        self.spielart = spielart
        self.spiel = None

        # modifizierte Hauptschleife, die auch Spiellogik ausführt
        self.running = True
        self.hauptschleife_id = None

        self.interface_generieren()

        if spielart == "Simulation":
            self.spiel_starten(None)
        elif spielart in ["Klassisch", "Wandlos", "Gegen Computer"]:
                if name := self.config["Spiel"]["nutzername"]:
                    self.spiel_starten([name])
                else:
                    NameEingabeFenster(self, 1)  # Das NameEingabeFenster ruft nach dem Beenden der Eingabe dann spiel_starten() auf.
        elif spielart == "Mehrspieler":
            NameEingabeFenster(self, 2)

    def spiel_starten(self, namen: list[str] = None) -> None:
        """
        Startet das Spiel mit den gegebenen Namen.

        :param namen: Liste der Namen der Spieler
        :return:
        """

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

    def taste(self, event: Event) -> None:
        """
        Verarbeitet die Tastatureingaben.
        Tastatureingaben sollen an das Spiel weitergeleitet werden, sodass Benutzerinteraktion möglich ist.

        :param event: Tkinter <Key> Event
        :return:
        """

        taste = event.char

        if taste == "\x1b":  # Escape
            self.running = False
            self.pausieren()
            return

        if taste in self.spiel.erlaubte_eingaben:
            self.eingaben.append(taste)

        logger.debug(f"{taste} {taste in self.spiel.erlaubte_eingaben}")

    def interface_generieren(self) -> None:
        """
        Generiert die Oberfläche des SpielFensters.

        :return:
        """

        super().interface_generieren()
        self.frame.pack(expand=True, fill=BOTH)  # soll sich auch in y-Richtung ausdehnen

        # Spielfeld
        self.spielfeld = Frame(self.frame)
        self.spielfeld.grid_columnconfigure(tuple(range(self.w)), weight=1)  # expand
        self.spielfeld.grid_rowconfigure(tuple(range(self.h)), weight=1)
        self.spielfeld.pack(expand=True, fill=BOTH)

        for x in range(self.w):
            for y in range(self.h):
                kachel = Label(self.spielfeld)
                kachel.grid(column=x, row=y, sticky="NESW")
                self.kacheln[x][y] = kachel

    def _kachel(self, column: int, row: int) -> None:
        """
        Gibt das Widget in der Zelle (column, row) zurück.
        Derzeit nicht in verwendung. Suboptimale Lösung, da jedes Mal ein Suchvorgang stattfindet.

        :param column: Reihennummer
        :param row: Spaltennummer
        :return:
        """

        try:
            # Es gibt nur ein Objekt in der Zelle, und das ist der Frame.
            return self.spielfeld.grid_slaves(column=column, row=row)[0]
        except Exception as e:
            logger.exception(e)

    def kachel_faerben(self, x: int, y: int, farbe: str) -> None:
        """
        Faerbt die Kachel (x, y) in der gegebenen Farbe.

        :param x: x-Koordinate
        :param y: y-Koordinate
        :param farbe: Farbe
        :return:
        """

        if not ((0 <= x <= self.w - 1) and (0 <= y <= self.h - 1)):
            logger.warning(f"Kachel ({x}, {y}) liegt außerhalb des Spielfelds")
            return

        # Manchmal gibt es hier Probleme mit persistenten referenzen von Widgets seitens tcl.
        # Die entsprechenden Objekte werden womöglich nicht sachgemäß vom Garbage Collector gelöscht?
        # Daher wird das Spiel nach Beendung auch vollständig neu gestartet.
        try:
            kachel = self.kacheln[x][y]
            if kachel and kachel.winfo_exists():
                kachel.config(background=farbe)
            else:
                logger.warning(f"Kachel ({x}, {y}) existiert nicht mehr.")
        except Exception as e:
            logger.exception(f"self.kacheln : {e}")

    def hauptschleife(self) -> None:
        """
        Hauptschleife des Spiels. Wird in einem separaten Thread ausgeführt.

        :return:
        """

        if self.running:
            try:
                self.spiel.aktualisieren()
                self.update()
            except Exception as e:
                logger.error(e)

            # separater Thread, um mainloop nicht zu blockieren
            self.hauptschleife_id = self.after(self.spiel.delay, self.hauptschleife)
    
    def pausieren(self) -> None:
        """
        Pausiert das Spiel.

        :return:
        """

        PauseFenster(self)

    def schliessen(self) -> None:
        """
        Plant das tatsächliche Schliessen, sodass die (separate) Hauptschleife nicht mehr läuft,
        wenn die dort referenzierten Objekte bereits gelöscht wurden.

        :return:
        """

        self.running = False
        # Hauptschleife (Thread) auslaufen lassen, sodass keine gelöschten Variablen referenziert werden
        self.after(100, self._schliessen)

    def _schliessen(self) -> None:
        """
        Schließt das SpielFenster und öffnet das Auswertungsfenster.

        :return:
        """

        self.destroy()
        AuswertungFenster(self.hauptfenster, self.spiel)

        # zirkulaere Refenz entfernen
        self.spiel.spiel_fenster = None
        self.spiel = None
        del self.spiel
        del self
