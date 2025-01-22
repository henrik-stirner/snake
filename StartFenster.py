import tkinter as tk


def main(): 
    root = tk.Tk()

    root.title("Tk Example")
    root.configure(background="black")
    root.minsize(1600, 900)
    root.minsize(1600, 900)
    root.geometry("1600x900+100+100")

    frame = tk.Frame(root, padx=100, pady=100)
    frame.pack(padx=10, pady=10)

    win = tk.Button(frame, width=160,height=15, text="Du fetter Oger",font="Arial 16 bold")
    win.pack()
    
    root.mainloop()


if __name__ == "__main__": 
    main()
