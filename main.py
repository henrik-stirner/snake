from typing import *

from os import walk, remove
from datetime import datetime
import logging
from logging.config import fileConfig

from configparser import ConfigParser

from tkinter import *
from tkinter import messagebox
# from tkinter.ttk import *  # FÜR STYLES!!!

from random import randint

from utils import *


# ----------
# logging
# ----------


"""
----------
USAGE
----------
display output for ordinary cli:
    print()
report events (status monitoring, fault investigation):
    logger.info() or
    logger.debug() for detailed output
issue warnings (particular runtime events):
    issue is avoidable and the code should be modified:
        warnings.warn()
    the event should be noticed, but there is nothing you can do about it:
        logger.warning()
report errors (particular runtime events):
    catch Error/
    raise MostSpecificError()
report suppressed errors without raising exceptions:
    logger.error() or
    logger.exception() or
    logger.critical()
----------
"""


logging.config.fileConfig(
            './logger.ini',
            encoding='utf-8',
            defaults={
                'logfilename':
                    f'./logs/{datetime.now().strftime("%Y-%m-%d_-_%H-%M-%S")}.log'
            }
        )
logger = logging.getLogger(__name__)

# only keep up to 5 log files
logfiles = list(filter(
    lambda file: file.endswith('.log') or file.split('.')[-1].isdigit(),
    next(walk('./logs/'), (None, None, []))[2]
))
if len(logfiles) > 5:
    for logfile in logfiles[0:len(logfiles) - 5]:
        remove(f'./logs/{logfile}')
del logfiles


# ----------
# config
# ----------


config = ConfigParser()
config.read("./config.ini")


# ----------
# game
# ----------


class SpielObjekt:
    def __init__(self, spiel, x, y, farbe, lebensdauer=None):
        self.spiel = spiel

        self.x = x
        self.y = y

        self.farbe = farbe

        self.tot = False
        self.lebensdauer: int | None = lebensdauer

    def aktualisieren(self):
        if self.lebensdauer is not None:
            if self.lebensdauer == 0:
                self.farbe = "black"
                self.tot = True
            else:
                self.lebensdauer -= 1

    def malen(self):
        self.spiel.spiel_fenster.kachel_faerben(self.x, self.y, self.farbe)


class Apfel(SpielObjekt):
    def __init__(self, spiel, x, y):
        super().__init__(spiel, x, y, "red")


class SchlangenGlied(SpielObjekt):
    def __init__(self, spiel, schlangenkopf, lebensdauer):
        super().__init__(spiel, schlangenkopf.x, schlangenkopf.y, "green", lebensdauer=lebensdauer)


class SchlangenKopf(SpielObjekt):
    def __init__(self, spiel, x, y, richtung, laenge):
        super().__init__(spiel, x, y, "darkgreen")

        # links, rechts, oben, unten
        self.richtung = richtung
        self.laenge = laenge

    def aktualisieren(self):
        super().aktualisieren()

        if self.laenge:
            neues_schlangenglied = SchlangenGlied(self.spiel, self, self.laenge)
            self.spiel.spielobjekte.append(neues_schlangenglied)

        match self.richtung:
            case "l":
                if self.x > 0:
                    self.x -= 1
            case "r":
                if self.x < self.spiel.spiel_fenster.w-1:
                    self.x += 1
            case "o":
                if self.y > 0:
                    self.y -= 1
            case "u":
                if self.y < self.spiel.spiel_fenster.h-1:
                    self.y += 1

        # TODO: Kollisionen


class Spiel:
    spielobjekte = []

    def __init__(self, spiel_fenster):
        self.spiel_fenster = spiel_fenster

        self.schlange = SchlangenKopf(self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaelliges_freies_feld())

        self.spielobjekte += [self.schlange, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot:
                self.spielobjekte.remove(spielobjekt)

        if self.spiel_fenster.eingaben:
            if "\x1b" in self.spiel_fenster.eingaben:  # Escape
                self.spiel_fenster.beenden()
                return

            eingabe = self.spiel_fenster.eingaben.pop(0)
            match eingabe:
                case "w":
                    self.schlange.richtung = "o"
                case "a":
                    self.schlange.richtung = "l"
                case "s":
                    self.schlange.richtung = "u"
                case "d":
                    self.schlange.richtung = "r"

        for spielobjekt in self.spielobjekte:
            spielobjekt.aktualisieren()
            spielobjekt.malen()

    def zufaelliges_feld(self):
        x = randint(0, self.spiel_fenster.w-1)
        y = randint(0, self.spiel_fenster.h-1)

        return x, y

    def feld_frei(self, x, y):
        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                return False

        return True

    def zufaelliges_freies_feld(self):
        x, y = self.zufaelliges_feld()
        # TODO: Was, wenn kein Feld mehr frei ist?
        while not self.feld_frei(x, y):
            x, y = self.zufaelliges_feld()

        return x, y


class SpielFenster(Toplevel):
    w, h = int(config["Game"]["w"]), int(config["Game"]["h"])
    delay = float(config["Game"]["delay"])
    erlaubte_tasten = "wasd"
    eingaben = []

    def __init__(self, launcher_fenster) -> None:
        super().__init__(launcher_fenster)

        self.focus_force()

        self.launcher_fenster = launcher_fenster

        self.spiel = Spiel(self)

        self.title("Spiel")
        self.configure(background="black")
        # root.minsize(config["Window"]["w"], config["Window"]["h"])
        self.geometry(
            f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}"
        )
        self.protocol("WM_DELETE_WINDOW", self.beenden)

        self.spielfeld = Frame(self)
        self.spielfeld.grid_columnconfigure(tuple(range(self.w)), weight=1)  # expand
        self.spielfeld.grid_rowconfigure(tuple(range(self.h)), weight=1)
        self.spielfeld.pack(expand=True, fill=BOTH)

        # Farbe der Labels beim Hovern veraender, sodass man das Raster besser erkennen kann (interaktiver)
        mod = 0x111111  # Unterschied zwischen den Farben

        def on_enter(obj, event):
            rgb = get_rgb_int(obj)
            rgb += mod
            if rgb > 0xFFFFFF:
                rgb = 0xFFFFFF
            color = int_to_hex_str(rgb)
            obj.config(bg=color)  # change background on hover

        def on_leave(obj, event):
            rgb = get_rgb_int(obj)
            rgb -= mod
            if rgb < 0:
                rgb = 0
            color = int_to_hex_str(rgb)
            obj.config(bg=color)  # reset background when mouse leaves

        self.kacheln = [[None for _ in range(self.h)] for _ in range(self.w)]
        for x in range(self.w):
            for y in range(self.h):
                kachel = Label(self.spielfeld, bg="black", width=1, height=1)
                kachel.grid(column=x, row=y, sticky="NESW")
                kachel.bind("<Enter>", lambda event, obj=kachel: on_enter(obj, event))
                kachel.bind("<Leave>", lambda event, obj=kachel: on_leave(obj, event))
                self.kacheln[x][y] = kachel

        # Eingaben verarbeiten
        def bei_tastendruck(event):
            taste = event.char
            if taste in self.erlaubte_tasten:
                self.eingaben.append(taste)
                logger.info(self.eingaben)

        self.bind('<Key>', bei_tastendruck)

        # modifizierte Hauptschleife, die auch Spiellogik ausfuehrt
        self.running = True
        self.hauptschleife_id = None

        self.hauptschleife()

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
                kachel.config(bg=farbe)
            else:
                logger.warning(f"Kachel ({x}, {y}) existiert nicht mehr.")
        except Exception as e:
            logger.error(e)

    def beenden(self):
        beenden = messagebox.askyesno("Beenden?", "Wollen Sie das Spiel wirklich beenden?")
        if beenden:
            self.running = False
            # sicherstellen, dass attribute nicht nach dem Schließen noch referenziert werden
            self.after_cancel(self.hauptschleife_id)
            self.after(100, self.schliessen)

    def schliessen(self):
        if not self.running:
            self.destroy()
            self.launcher_fenster.deiconify()

    def hauptschleife(self):
        if self.running:
            try:
                self.spiel.aktualisieren()
            except Exception as e:
                logger.error(e)

            # seperater thread, um mainloop nicht zu blockieren
            self.hauptschleife_id = self.after(int(self.delay * 500), self.hauptschleife)


class Launcher(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.focus_force()

        self.spiel_fenster = None

        self.title("Launcher")
        self.configure(background="black")
        # root.minsize(config["Window"]["w"], config["Window"]["h"])
        self.geometry(
            f"{config['Window']['w']}x{config['Window']['h']}+{config['Window']['x']}+{config['Window']['y']}"
        )

        self.interface_generieren()

        self.mainloop()

    def interface_generieren(self) -> None:
        # Schlange

        self.schlange_frame = Frame(self)
        self.schlange_frame.pack(expand=True)

        self.schlange = Frame(self.schlange_frame, width=500, height=100)
        self.schlange.grid_columnconfigure(tuple(range(5)), weight=1)
        self.schlange.grid_rowconfigure(0, weight=1)
        self.schlange.pack_propagate(0)
        self.schlange.pack()

        farbe = 0x2EbA18
        for buchstabe in "SNAKE":
            buchstabe_label = Label(self.schlange, text=buchstabe, font=config["Font"]["text"],
                                    fg="white", bg=f"#{hex(farbe).removeprefix('0x')}")
            buchstabe_label.pack(side=LEFT, expand=True, fill=BOTH)
            farbe += 16

        # Startknopf

        self.start_knopf = Button(self, command=self._on_start,
                                  text="START", font=config["Font"]["huge"], height=5,
                                  bg="black", fg="white", activeforeground="black", activebackground="white",
                                  highlightthickness=0, bd=0)
        self.start_knopf.pack(fill=X)

        # Ranking

        self.ranking_frame = Frame(self, bg="black")
        self.ranking_frame.pack(expand=True)

        with open("scores.txt", "r") as lesedatei:
            highscores = [(int(zeile.split()[0]), zeile) for zeile in lesedatei.readlines()]
            highscores.sort(key=lambda x: x[0], reverse=True)

            for highscore in highscores[:5]:
                score_label = Label(self.ranking_frame, text=highscore[1], font=config["Font"]["head"],
                                    fg="white", bg="black")
                score_label.pack(expand=True, fill=BOTH)

    def _on_start(self):
        self.withdraw()  # launcher_fenster verstecken
        SpielFenster(self)


def main(): 
    Launcher()


if __name__ == "__main__": 
    main()
