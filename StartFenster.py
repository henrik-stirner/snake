import tkinter as tk


def main(): 
    root = tk.Tk()

    root.title("Tk Example")
    root.configure(background="black")
    root.minsize(1600, 900)
    root.geometry("1600x900+100+100")

    main_frame = tk.Frame(root, bg="black", padx=100, pady=100)
    main_frame.grid(row=0, column=0)  # Hier grid() anstelle von pack() verwenden
    
    # Schlange

    schlange_frame = tk.Frame(main_frame, bg="black")
    schlange_frame.grid(row=0, column=0)
    
    s_label = tk.Label(schlange_frame, width=10, height=10, text="S", bg="darkgreen")
    s_label.grid(row=0, column=0)
    n_label = tk.Label(schlange_frame, width=10, height=10, text="N", bg="lightgreen")
    n_label.grid(row=0, column=1)
    a_label = tk.Label(schlange_frame, width=10, height=10, text="A", bg="lightgreen")
    a_label.grid(row=0, column=2)
    k_label = tk.Label(schlange_frame, width=10, height=10, text="K", bg="lightgreen")
    k_label.grid(row=0, column=3)
    e_label = tk.Label(schlange_frame, width=10, height=10, text="E", bg="lightgreen")
    e_label.grid(row=0, column=4)
    
    # Ranking

    ranking_frame = tk.Frame(main_frame, bg="black")
    ranking_frame.grid(row=1, column=0)
    
    # Startknopf

    start_knopf = tk.Button(main_frame, bg="darkgrey", activebackground="#3e393e", width=16, height=9, text="START",font="Arial 16 bold")
    start_knopf.grid(row=2, column=0)
    
    root.mainloop()


if __name__ == "__main__": 
    main()
