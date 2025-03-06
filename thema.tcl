ttk::style theme create dunkel -parent clam -settings {
    ttk::style configure . -background black

    ttk::style configure TFrame -background black

    ttk::style configure TLabel -background black -foreground white -font "Arial 12"

    ttk::style configure TButton -background #222 -foreground white -font "Arial 12 bold" -padding 5
    ttk::style map TButton -background [list active #444 pressed #666]
}