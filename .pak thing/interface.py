import tkinter

w = tkinter.Tk()
w.title("PakMan")
w.resizable(False,False)
btn = tkinter.Button(w, text="Launch .pak Explorer", fg="black", height=5, width=20, font=("Times New Roman", 12)).place(x=100, y=100)
title = tkinter.Label(w, text = "Welcome to PakExplorer v0.1 !", font=("Times New Roman bold", 12)).pack(pady=10)

w.geometry("800x700+300+0")
















w.mainloop()