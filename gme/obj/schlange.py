from typing import *
from configparser import ConfigParser
import logging


# ----------
# config und logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.base import SpielObjekt
from gme.obj.konsumgut import Konsumgut

# ----------


class SchlangenGlied(SpielObjekt):
    def __init__(self, spiel, schlangenkopf, farbe, lebensdauer):
        super().__init__(spiel, schlangenkopf.x, schlangenkopf.y, farbe, 1, lebensdauer)

        self.kopf = schlangenkopf

    def aktualisieren(self):
        if self.kopf.tot:
            self.tot = True

        super().aktualisieren()


class SchlangenKopf(SpielObjekt):
    erlaubte_richtungen = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def __init__(self, name, spiel, x, y, richtung, laenge, farbe="darkgreen", lebensdauer=None, wand_teleport=False):
        super().__init__(spiel, x, y, farbe, 2, lebensdauer)

        self.wand_teleport = wand_teleport

        self.name = name
        self.gliedfarbe = self.farbe.removeprefix("dark") if self.farbe.startswith("dark") else self.farbe

        self.richtung = richtung
        self.laenge = laenge

    def drehen(self, neue_richtung: tuple[int, int]):
        # 180-Grad-Wende verhindern
        if self.richtung[0] == -neue_richtung[0] and self.richtung[1] == -neue_richtung[1]:
            return

        self.richtung = neue_richtung

    def aktualisieren(self):
        # AUSGANGSFELD

        # Konsum
        if spielobjekte := self.spiel.objekte_auf_kachel(self.x, self.y):
            for spielobjekt in spielobjekte:
                if isinstance(spielobjekt, Konsumgut) and not spielobjekt.konsumiert:
                    self.laenge += spielobjekt.wertigkeit
                    spielobjekt.konsumiert = True

        # Bombe
        if self.laenge:
            neues_schlangenglied = SchlangenGlied(self.spiel, self, self.gliedfarbe, self.laenge)
            self.spiel.spielobjekte.append(neues_schlangenglied)

        # Bewegen: NACH BOMBE UND KONSUM
        self.x += self.richtung[0]
        self.y += self.richtung[1]

        # EIN FELD WEITER

        if not all([isinstance(obj, Konsumgut) or obj == self for obj in self.spiel.objekte_auf_kachel(self.x, self.y)]):
            # in Schlange gefahren
            self.tot = True
        elif self.wand_teleport:
            if self.x < 0:
                self.x = self.spiel.spiel_fenster.w - 1
            elif self.x > self.spiel.spiel_fenster.w - 1:
                self.x = 0
            if self.y < 0:
                self.y = self.spiel.spiel_fenster.h - 1
            elif self.y > self.spiel.spiel_fenster.h - 1:
                self.y = 0
        elif not (0 <= self.x <= self.spiel.spiel_fenster.w - 1) or not (0 <= self.y <= self.spiel.spiel_fenster.h - 1):
            self.tot = True

        super().aktualisieren()
