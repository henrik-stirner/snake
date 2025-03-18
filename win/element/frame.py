from tkinter import Canvas, VERTICAL, BOTH, LEFT, RIGHT, FALSE, TRUE, NW, Y
from tkinter.ttk import *


class VerticalScrolledFrame(Frame):
    """
    A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    Kopiert aus: https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
    """

    def __init__(self, parent, *args, **kw):
        """
        Initialisierung des vertikal scrollbaren Frames.

        :param parent:
        :param args:
        :param kw:
        """

        Frame.__init__(self, parent, *args, **kw)

        # Ergaenzung
        window = parent.winfo_toplevel()
        stil = window.stil
        # ----------

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Ergaenzung: automatische Anpassung der Hintergrundfarbe;
        # kann nicht mit Stylesheet stilisiert werden (kein Teil von ttk)
        canvas.config(bg=stil.lookup("TFrame", "background"))
        # ----------

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            """
            Konfiguriert den inneren Frame.
            Das Canvas-Objekt wird an die Größe des inneren Frames angepasst,
            ebenso die Scrollbar des Canvas-Objekts.
            .
            :param event:
            :return:
            """

            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion=f"0 0 {size[0]} {size[1]}")
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            """
            Konfiguriert das Canvas-Objekt.
            Auch wenn sich das Canvas-Objekt ändert, wird der innere Frame angepasst,
            nicht nur umgekehrt.

            :param event:
            :return:
            """

            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

        return
