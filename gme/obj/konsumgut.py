from typing import *
import logging


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.base import SpielObjekt

# ----------


class Konsumgut(SpielObjekt):
    """
    konsumierbares SpielObjekt einer bestimmten Wertigkeit
    """

    def __init__(self, spiel: object, x: int, y: int, farbe: str, wertigkeit: int, lebensdauer: int = None) -> None:
        """
        Initialisiert ein neues Konsumgut.

        :param spiel: Spiel, in dem das Objekt existieren soll
        :param x: x-Koordinate
        :param y: y-Koordinate
        :param farbe: Farbe des Objekts
        :param wertigkeit: Wertigkeit des Konsumguts (um wie viel sich die Schlange durch den Konsum verlängert)
        :param lebensdauer: Lebensdauer des Objekts in Zyklen (Aktualisierungen des Spielfelds). Standard: None (unendlich)
        """

        super().__init__(spiel, x, y, farbe, 0, lebensdauer=lebensdauer)

        self.aktive_farbe = farbe
        self.konsumiert = False
        self.wertigkeit = wertigkeit

    def malen(self) -> None:
        """
        Wenn das Konsumgut gegessen wurde, wird es schwarz dargestellt.
        :return:
        """

        self.farbe = self.aktive_farbe if not self.konsumiert else "black"
        super().malen()


class Apfel(Konsumgut):
    """
    Konsumgut der Wertigkeit 1 und der Farbe "red"
    """

    def __init__(self, spiel: object, x: int, y: int) -> None:
        """
        Initialisiert einen neuen Apfel.

        :param spiel: Spiel, in dem das Objekt existieren soll
        :param x: x-Koordinate
        :param y: y-Koordinate
        """

        super().__init__(spiel, x, y, "red", 1)

    def aktualisieren(self) -> None:
        """
        Wenn der Apfel konsumiert wurde, wird er auf eine zufällige freie Kachel gesetzt und wieder aktiviert.

        :return:
        """

        if self.konsumiert:
            nx, ny = self.spiel.zufaellige_freie_kachel()
            if nx is None:
                self.spiel.spiel_beenden()
                return
            self.x, self.y = nx, ny

            self.konsumiert = False
        
        super().aktualisieren()
