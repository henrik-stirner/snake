import tkinter as tk
from configparser import ConfigParser


config = ConfigParser()
config.read("./config.ini")

def start_fenster():
    root = tk.Tk()

    root.title("Snake")
    root.configure(background="black")
    # root.minsize(config["Window"]["w"], config["Window"]["h"])
    root.geometry(f"{config["Window"]["w"]}x{config["Window"]["h"]}+{config["Window"]["x"]}+{config["Window"]["y"]}")

    # Schlange

    schlange_frame = tk.Frame(root)
    schlange_frame.pack(expand=True)

    schlange = tk.Frame(schlange_frame, width=500, height=100)
    schlange.grid_columnconfigure(tuple(range(5)), weight=1)
    schlange.grid_rowconfigure(0, weight=1)
    schlange.pack_propagate(0)
    schlange.pack()

    farbe = 0x2EbA18
    for buchstabe in "SNAKE":
        buchstabe_label = tk.Label(schlange, text=buchstabe, font=config["Font"]["text"],
                                   fg="white", bg=f"#{hex(farbe).removeprefix('0x')}")
        buchstabe_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        farbe += 16

    # Startknopf

    start_knopf = tk.Button(root, text="START", font=config["Font"]["huge"], height=5,
                            bg="black", fg="white", activeforeground="black", activebackground="white",
                            highlightthickness=0, bd=0)
    start_knopf.pack(fill=tk.X)

    # Ranking

    ranking_frame = tk.Frame(root, bg="black")
    ranking_frame.pack(expand=True)

    for i in range(5):
        score_label = tk.Label(ranking_frame, text="Score [Name] und weitere Daten", font=config["Font"]["head"],
                               fg="white", bg="black")
        score_label.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

def main(): 
    start_fenster()


if __name__ == "__main__": 
    main()
