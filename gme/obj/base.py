from typing import *
from configparser import ConfigParser
import logging


# ----------
# logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

# ...

# ----------


class SpielObjekt:
    """
    Ein Spielobjekt, das im Spiel existiert.
    """

    def __init__(self, spiel: object, x: int, y: int, farbe: str, z_index: int = 0, lebensdauer: int = None) -> None:
        """
        Initialisiert ein neues Spielobjekt.

        :param spiel: Spiel, in dem das Objekt existieren soll
        :param x: x-Koordinate
        :param y: y-Koordinate
        :param farbe: Farbe des Objekts
        :param z_index: Z-Index des Objekts (Reihenfolge der Darstellung: Ein höherer Z-Index bedeutet, dass das Objekt über anderen Objekten gezeichnet wird)
        :param lebensdauer: Lebensdauer des Objekts in Zyklen (Aktualisierungen des Spielfelds). Standard: None (unendlich)
        """

        self.spiel = spiel

        self.x = x
        self.y = y

        self.farbe = farbe
        self.z_index = z_index

        self.tot = False
        self.lebensdauer: int | None = lebensdauer

    def aktualisieren(self) -> None:
        """
        Aktualisiert das Spielobjekt.
        Wird einmal pro Zyklus aufgerufen, vor dem Malen.

        :return:
        """

        if self.lebensdauer is not None:
            if self.lebensdauer == 0:
                self.tot = True
            else:
                self.lebensdauer -= 1

        if self.tot:
            self.farbe = "black"

    def malen(self) -> None:
        """
        Malt das Spielobjekt.
        Wird einmal pro Zyklus aufgerufen, nach dem Aktualisieren.

        :return:
        """

        self.spiel.spiel_fenster.kachel_faerben(self.x, self.y, self.farbe)
