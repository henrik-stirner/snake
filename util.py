from tkinter import X, Y, LEFT, RIGHT, TOP, BOTTOM, BOTH
from tkinter.ttk import *


def schlange(parent, text):
	schlange = Frame(parent, width=500, height=100)
	schlange.grid_columnconfigure(tuple(range(5)), weight=1)
	schlange.grid_rowconfigure(0, weight=1)
	schlange.pack_propagate(False)
	schlange.pack()

	farbe = 0x2EbA18
	for buchstabe in text:
		hex_code = f"#{hex(farbe).removeprefix('0x')}"

		stil = Style()
		stil.configure("Custom.TFrame", background=hex_code)

		buchstabe_frame = Frame(schlange, style="Custom.TFrame")
		buchstabe_frame.pack(side=LEFT, expand=True, fill=BOTH)

		buchstabe_label = Label(buchstabe_frame, text=buchstabe, background=hex_code)
		buchstabe_label.pack(expand=True)

		farbe += 16

	return schlange
