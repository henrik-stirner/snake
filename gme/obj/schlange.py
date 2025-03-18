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

from gme.obj.base import SpielObjekt
from gme.obj.konsumgut import Konsumgut

# ----------


class SchlangenGlied(SpielObjekt):
    """
    Schlangenglied, das vom Schlangenkopf hinterlassen wird.
    Überlebt so viele Spielzyklen bzw. Aktualisierungen, wie die Schlange lang ist.
    """

    def __init__(self, spiel: object, schlangenkopf: object, farbe: str, lebensdauer: int) -> None:
        """
        Initialisiert ein Schlangenglied.

        :param spiel: Spiel, in dem das Objekt existieren soll
        :param schlangenkopf: Schlangenkopf, der das Schlangenglied hinterlassen hat
        :param farbe: Farbe des Objekts
        :param lebensdauer: Lebensdauer des Objekts in Zyklen (Aktualisierungen des Spielfelds). Standard: None (unendlich)
        """
        super().__init__(spiel, schlangenkopf.x, schlangenkopf.y, farbe, 1, lebensdauer)

        self.kopf = schlangenkopf

    def aktualisieren(self) -> None:
        """
        Das Schlangenglied stirbt, wenn der Schlangenkopf stirbt.

        :return:
        """

        if self.kopf.tot:
            self.tot = True

        super().aktualisieren()


class SchlangenKopf(SpielObjekt):
    """
    SpielObjekt, das sich in eine Richtung bewegt und Schlangenglieder hinterlässt.
    Die Richtung bestimmt im Normalfall der Spieler.
    """

    erlaubte_richtungen = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def __init__(self, name: str, spiel: object, x: int, y: int, richtung: tuple[int, int], laenge: int, farbe: str = "darkgreen", lebensdauer: int = None, wand_teleport: bool = False) -> None:
        """
        Initialisiert einen Schlangenkopf.

        :param name: Name des Spielers
        :param spiel: Spiel, in dem das Objekt existieren soll
        :param x: x-Koordinate
        :param y: y-Koordinate
        :param richtung: 2d-Richtungsvektor, in welche sich das Objekt bewegen soll [z.B. (1, 0) für rechts]
        :param laenge: Länge der Schlange
        :param farbe: Farbe des Objekts. Standard: "darkgreen". Vorzugsweise eine dunkle Farbe (Glieder standardmäßig heller, z.B. "green").
        :param lebensdauer: Lebensdauer des Objekts in Zyklen (Aktualisierungen des Spielfelds). Standard: None (unendlich)
        :param wand_teleport: Ob der Schlangenkopf durch die Wand teleportiert wird. Standard: False (Wände tödlich)
        """

        super().__init__(spiel, x, y, farbe, 2, lebensdauer)

        self.wand_teleport = wand_teleport

        self.name = name
        self.gliedfarbe = self.farbe.removeprefix("dark") if self.farbe.startswith("dark") else self.farbe

        self.richtung = richtung
        self.laenge = laenge

    def drehen(self, neue_richtung: tuple[int, int]) -> None:
        """
        Ändert die Richtung des Schlangenkopfes, nach Prüfung derer Gültigkeit.
        Die Richtung wird nur geändert, wenn sie der derzeitigen nicht 180 Grad entgegengesetzt ist.

        :param neue_richtung:
        :return:
        """

        # 180-Grad-Wende verhindern
        if self.richtung[0] == -neue_richtung[0] and self.richtung[1] == -neue_richtung[1]:
            return

        self.richtung = neue_richtung

    def aktualisieren(self):
        """
        Der Schlangenkopf bewegt sich in die aktuelle Richtung und verlängert sich, wenn er ein Konsumgut konsumiert hat.

        :return:
        """

        # AUSGANGSFELD

        # Konsum
        if spielobjekte := self.spiel.objekte_auf_kachel(self.x, self.y):
            for spielobjekt in spielobjekte:
                if isinstance(spielobjekt, Konsumgut) and not spielobjekt.konsumiert:
                    self.laenge += spielobjekt.wertigkeit
                    spielobjekt.konsumiert = True

        # Schlangenglied
        if self.laenge:
            neues_schlangenglied = SchlangenGlied(self.spiel, self, self.gliedfarbe, self.laenge)
            self.spiel.spielobjekte.append(neues_schlangenglied)

        # Bewegen?
        nx = self.x + self.richtung[0]
        ny = self.y + self.richtung[1]

        # EIN FELD WEITER

        if not all([isinstance(obj, Konsumgut) or obj == self for obj in self.spiel.objekte_auf_kachel(nx, ny)]):
            # in Schlange gefahren
            self.tot = True
        elif self.wand_teleport:
            if nx < 0:
                nx = self.spiel.spiel_fenster.w - 1
            elif nx > self.spiel.spiel_fenster.w - 1:
                nx = 0
            if ny < 0:
                ny = self.spiel.spiel_fenster.h - 1
            elif ny > self.spiel.spiel_fenster.h - 1:
                ny = 0
        elif not (0 <= nx <= self.spiel.spiel_fenster.w - 1) or not (0 <= ny <= self.spiel.spiel_fenster.h - 1):
            self.tot = True

        if not self.tot:
            # Die Schlange soll das Spielfeld auch im toten Zustand nicht verlassen können.
            self.x, self.y = nx, ny

        super().aktualisieren()
