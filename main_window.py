from tkinter import *
from tkinter import ttk, messagebox, filedialog


class Window:
    def __init__(self):
        self.master = Tk()
        self.master.title("SPH - PDV")
        self.master.minsize(800, 600)
        self.variables()
        self.master.mainloop()
        
    def variables(self):
        print(self.main_bg)

if __name__ == "__main__":
    run = Window()