from typing import *
from configparser import ConfigParser
import logging

from tkinter import *
from tkinter import messagebox

from utils import *
from gme.klassisch import KlassischerModus

# ----------
# config und logger
# ----------


config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)


# ----------


class SpielFenster(Toplevel):
    w, h = int(config["Game"]["w"]), int(config["Game"]["h"])
    delay = float(config["Game"]["delay"])
    erlaubte_tasten = "wasd"
    eingaben = []

    def __init__(self, launcher_fenster) -> None:
        super().__init__(launcher_fenster)

        self.focus_force()

        self.launcher_fenster = launcher_fenster

        self.spiel = KlassischerModus(self)

        self.title("gme")
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
        beenden = messagebox.askyesno("Beenden?", "Wollen Sie das gme wirklich beenden?")
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
