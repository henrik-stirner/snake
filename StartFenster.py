from tkinter import *
from tkinter import messagebox
# from tkinter.ttk import *  # FÜR STYLES!!!

from configparser import ConfigParser

from utils import *


config = ConfigParser()
config.read("./config.ini")


class Launcher:
    def __init__(self) -> None:
        self.launcher_fenster = Tk()

        self.launcher_fenster.title("Launcher")
        self.launcher_fenster.configure(background="black")
        # root.minsize(config["Window"]["w"], config["Window"]["h"])
        self.launcher_fenster.geometry(
            f"{config['Window']['w']}x{config['Window']['h']}+{config['Window']['x']}+{config['Window']['y']}"
        )

        self.interface_generieren()

        self.launcher_fenster.mainloop()

    def interface_generieren(self) -> None:
        # Schlange

        self.schlange_frame = Frame(self.launcher_fenster)
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

        self.start_knopf = Button(self.launcher_fenster, command=self._on_start,
                                  text="START", font=config["Font"]["huge"], height=5,
                                  bg="black", fg="white", activeforeground="black", activebackground="white",
                                  highlightthickness=0, bd=0)
        self.start_knopf.pack(fill=X)

        # Ranking

        self.ranking_frame = Frame(self.launcher_fenster, bg="black")
        self.ranking_frame.pack(expand=True)

        for i in range(5):
            score_label = Label(self.ranking_frame, text="Score [Name] und weitere Daten", font=config["Font"]["head"],
                                   fg="white", bg="black")
            score_label.pack(expand=True, fill=BOTH)

    def _on_start(self):
        self.launcher_fenster.withdraw()  # launcher_fenster verstecken
        SpielFenster(self.launcher_fenster)


class SpielObjekt:
    def __init__(self, x, y, farbe):
        self.x = x
        self.y = y
        self.farbe = farbe

    def aktualisieren(self, **kwargs):
        pass


class SchlangenKopf(SpielObjekt):
    def __init__(self, spielfenster, x, y):
        super.__init__(x, y, "darkgreen")

        # links, rechts, oben, unten
        self.richtung: str
        self.glieder = []

    def aktualisieren(self, richtung):
        neues_schlangenglied = SchlangenGlied(self)
        self.glieder.append(neues_schlangenglied)

        if richtung:
            self.richtung = richtung

        match self.richtung:
            case "l":
                self.x -= 1
            case "r":
                self.x += 1
            case "o":
                self.y += 1
            case "u":
                self.y -= 1


class SchlangenGlied(SpielObjekt):
    def __init__(self, schlangenkopf):
        super().__init__(schlangenkopf.x, schlangenkopf.y, "darkgreen")


class Spiel:
    def __init__(self, spielfenster):
        self.spielfenster = spielfenster

        self.spielobjekte = []
        self.schlangenkopf = SpielObjekt(spielfenster, spielfenster.w // 2, spielfenster.h // 2, "darkgreen")
        self.spielobjekte.append(self.schlangenkopf)
        self.spielobjekte.append(self.schlangenkopf.glieder)

        while True:
            self.aktualisieren()

    def aktualisieren(self):
        if "q" in self.spielfenster.eingaben:
            self.spielfenster.window_exit()

        eingabe = self.spielfenster.eingaben[0]
        for spielobjekt in self.spielobjekte:
            spielobjekt.aktualisieren(eingabe)
        self.spielfenster.eingaben.pop(0)

        self.spielfenster.update_idletasks()


class SpielFenster:
    def __init__(self, root: Tk) -> None:
        self.spiel_fenster = Toplevel(root)
        self.spiel_fenster.title("Spiel")
        self.spiel_fenster.configure(background="black")
        # root.minsize(config["Window"]["w"], config["Window"]["h"])
        self.spiel_fenster.geometry(
            f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}"
        )
        self.spiel_fenster.protocol("WM_DELETE_WINDOW", self._window_exit)

        self.w, self.h = int(config["Game"]["w"]), int(config["Game"]["h"])

        self.spielfeld = Frame(self.spiel_fenster)
        self.spielfeld.grid_rowconfigure(tuple(range(self.h)), weight=1)  # expand
        self.spielfeld.grid_columnconfigure(tuple(range(self.w)), weight=1)
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

        for x in range(self.w):
            for y in range(self.h):
                kachel = Label(self.spielfeld, bg="black", width=1, height=1)
                kachel.grid(column=x, row=y, sticky="NESW")
                kachel.bind("<Enter>", lambda event, obj=kachel: on_enter(obj, event))
                kachel.bind("<Leave>", lambda event, obj=kachel: on_leave(obj, event))

        eine_kachel = self._kachel(3, 5)
        eine_kachel.config(bg="red")  # ein label rot, um zu sehen, ob es funktioniert

        # EINGABEN
        eingaben = []

        def tastendruck(event):
            taste = event.key
            self.eingaben.append(taste)
            print(taste)

        root.bind('<Key>', tastendruck)

    def kachel(self, row: int, column: int):
        return self.spielfeld.grid_slaves(row, column)[0]  # Es gibt nur ein Objekt in der Zelle, und das ist der Frame.

    def window_exit(self):
        close = messagebox.askyesno("Beenden?", "Wollen Sie das Spiel wirklich beenden?")

        if close:
            self.spiel_fenster.destroy()


def main(): 
    Launcher()


if __name__ == "__main__": 
    main()
