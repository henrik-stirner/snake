if {[tk windowingsystem] == "win32"} {
    set system_font "Segoe UI"
} elseif {[tk windowingsystem] == "x11" || [tk windowingsystem] == "wayland"} {
    set system_font "Ubuntu"
} elseif {[tk windowingsystem] == "aqua"} {  # macOS
    set system_font "San Francisco"
} else {  # Fallback
    set system_font "Arial"
}

set normal 12
set big 20

option add *font "\"$system_font\" 12 bold"

ttk::style theme create dunkel -parent clam -settings {
    # Frame
    ttk::style configure TFrame -background black

    # Label
    ttk::style configure TLabel -background black -foreground white -padding 5 -anchor center -justify center
    # weitere
    ttk::style configure Big.TLabel -font [list $system_font $big bold]

    # Button
    ttk::style configure TButton -background black -foreground white -anchor center -padding 50
    ttk::style map TButton -background [list active white] -foreground [list active black]
    # ----------
    ttk::style configure Big.TButton -font [list $system_font $big bold]
    # weitere
    ttk::style configure Ico.TButton -padding 5
    ttk::style map Ico.TButton -background [list active black]

    # Entry
    ttk::style configure TEntry -background black -foreground white -fieldbackground black -darkcolor white -lightcolor black -borderwidth 3 -relief flat -padding {10 5}

    # Combobox
    ttk::style configure TCombobox -background black -foreground white -fieldbackground black -lightcolor black -darkcolor black -arrowcolor white -arrowsize 17 -borderwidth 3 -relief flat -padding {10 5}
    # Liste
    option add *TCombobox*Listbox.background black
    option add *TCombobox*Listbox.foreground white
    option add *TCombobox*Listbox.selectBackground white
    option add *TCombobox*Listbox.selectForeground black
    # Frame der Liste
    # ttk::style configure ComboboxPopdownFrame -background black -borderwidth 0 -relief flat

    # Scrollbar
    ttk::style configure Vertical.TScrollbar -gripcount 0 -background black -troughcolor black -bordercolor black -arrowcolor white -arrowsize 17 -borderwidth 0 -relief flat -padding {10 5}
}