from tkinter import *
from tkinter import filedialog
import Lexer
import Parser

class IDE:

    def __init__(self):
        self.ideWindow = Tk()
        self.ideWindow.geometry("800x600+200+200")
        self.ideWindow.resizable(False, False)
        self.ideWindow.title("Esfera Compiladores")
        myCanvas = Canvas(self.ideWindow,
                          width="800", height="600",
                          bd=0, highlightthickness=0,
                          bg="#44287c")
        myCanvas.pack(fill="both", expand=True)
        self.row = 1
        self.ideWindow.bind("<F5>", lambda e: self.compile())
        self.ideWindow.bind("<Return>", lambda event: self.addRow())
        self.ideWindow.bind("<BackSpace>", lambda event2: self.checkRow())

    def topBar(self):
        menuBar = Menu(self.ideWindow)
        self.ideWindow.config(menu=menuBar)
        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Archivo", menu=fileMenu)
        fileMenu.add_command(label="Abrir", command=self.openFile)
        fileMenu.add_command(label="Guardar", command=self.saveFile)
        menuBar.add_command(label="Compilar", command=self.compile)
        menuBar.add_command(label="Ejecutar", command=self.runCompile)

    def codeEntry(self):
        self.entryBox = Text(self.ideWindow,
                              font=("Times New Romas", 16),
                              bg="#44287c",
                              fg="#dbd8bd", highlightthickness=1)

        self.entryBox.place(x=30, y=10, width=750, height=300)
        self.lineNum = Text(self.ideWindow, bg="#8c8599", font=("Times New Romans", 16), fg="#dbd8bd")
        self.lineNum.place(x=0, y=10, width=30, height=300)
        self.setLineText("1")
        self.lineNum.config(state=DISABLED)
        self.uniscrollbar = Scrollbar(self.ideWindow, orient="vertical", command=self.entryBox.yview)
        self.uniscrollbar.place(x=782, y=10, width=15)
        self.uniscrollbar.config(command=self.scrollBoth)
        self.entryBox.config(yscrollcommand=self.updateScroll)
        self.lineNum.config(yscrollcommand=self.updateScroll)

    def scrollBoth(self, action, position, type=None):
        self.entryBox.yview_moveto(position)
        self.lineNum.yview_moveto(position)

    def updateScroll(self, first, last, type=None):
        self.entryBox.yview_moveto(first)
        self.lineNum.yview_moveto(first)
        self.uniscrollbar.set(first, last)

    def codeOutput(self):
        self.outputBox = Text(self.ideWindow,
                              font=("Times New Romans", 16),
                              bg="#8c8599", bd=1,
                              fg="#dbd8bd", highlightthickness=1)
        self.outputBox.place(x=10, y=315, width=780, height=275)
        self.outputBox.config(state=DISABLED)

    def startIDE(self):
        self.topBar()
        self.codeEntry()
        self.codeOutput()
        self.ideWindow.mainloop()

    def openFile(self):
        path = filedialog.askopenfilename(initialdir="/",
                                          title="Abrir archivo",
                                          filetypes=(("text files", "*.txt"),
                                          ("All files", "*.*")))
        with open(path, "r") as f:
            cont = 1
            code = ""
            self.tmpText = ""
            for line in f:
                code += line
                cont = cont+1
            for num in range(1, cont):
                self.tmpText = self.tmpText + str(num) + "\n"
            self.lineNum.config(state=NORMAL)
            self.setLineText(self.tmpText)
            self.lineNum.config(state=DISABLED)
            self.setEntryCode(code)

    def setEntryCode(self, codeRaw):
        self.entryBox.delete('1.0', END)
        self.entryBox.insert(END, codeRaw)

    def getEntryCode(self):
        code = self.entryBox.get("1.0",END)
        return code

    def saveFile(self):
        path = filedialog.asksaveasfilename(initialdir="/", title=
                                            "Guardar como",
                                            filetypes=(("text files", "*.txt"),
                                            ("All files", "*.*")))
        file = open(path, "w")
        code = self.getEntryCode()
        file.write(code)
        file.close()

    def setLineText(self, numbersTxt):
        self.lineNum.delete('1.0', END)
        self.lineNum.insert(END, numbersTxt)

    def compile(self):
        self.outputBox.config(state=NORMAL)
        self.outputBox.delete('1.0',END)
        self.outputBox.update()
        file = open("compile.txt","w")
        code = self.getEntryCode()
        file.write(code)
        file.close()
        toks = Lexer.read_File("compile.txt")
        pars = Parser.readFile("compile.txt", False)
        self.outputBox.insert(END,(str(pars)+ "\n"))
        self.outputBox.config(state=DISABLED)
        Lexer.cleartoks()
        Parser.clearpars()
        pass
    def runCompile(self):
        pass

    def addRow(self):
        self.row = self.row + 1
        self.tmpText = ""
        for num in range(1, self.row + 1):
            self.tmpText = self.tmpText + str(num) + "\n"
        self.lineNum.config(state=NORMAL)
        self.setLineText(self.tmpText)
        self.lineNum.config(state=DISABLED)

    def deleteRow(self):
        if self.row == 1:
            self.row = 1
        else:
            self.row = self.row - 1

        self.tmpText = ""
        for num in range(1, self.row + 1):
            self.tmpText = self.tmpText + str(num) + "\n"
        self.lineNum.config(state=NORMAL)
        self.setLineText(self.tmpText)
        self.lineNum.config(state=DISABLED)

    def checkRow(self):
        content = self.entryBox.get("1.0","end")
        linebrake = content.count('\n')
        if self.row > int(linebrake):
            self.deleteRow()