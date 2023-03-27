from tkinter import *
from tkinter import filedialog
from Compilador import tokens

class IDE:
    def mainwindow(self):

        self.ideWindow = Tk()
        self.ideWindow.geometry("800x600+200+200")
        self.ideWindow.resizable(False,False)
        self.ideWindow.title("Esfera-Compi IDE")

        myCanvas= Canvas(self.ideWindow,
                         width = "800",
                         height= "600",
                         bd = 0,
                         highlightthickness=0,
                         bg="#44287c")
        myCanvas.pack(fill="both",expand=True)
        self.row = 1
        self.ideWindow.bind("<R>",lambda e:self.compile())

    def topBar(self):
        

