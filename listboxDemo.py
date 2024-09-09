from tkinter import *
import tkinter.font as tkFont


    


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.titlefont = tkFont.Font(family="Arial", size=20, slant="italic")
        self.buttonfont = tkFont.Font(family="Arial", size=18)
        self.listfont = tkFont.Font(family="Consolas", size=18)

        l1 = Label(self,text="Enter a new name", font=self.titlefont)
        l1.grid(row=0,column=0)
        self.newName = Entry(self,font = self.buttonfont)
        self.newName.grid(row=0, column=1)
        l2 = Label(self,text="Enter a new Score", font=self.titlefont)
        l2.grid(row=1,column=0)
        self.newScore = Entry(self,font = self.buttonfont)
        self.newScore.grid(row=1, column=1)

        b1 = Button(self,text="Add", command = self.addItem)
        b1.grid(row=2, column=0, columnspan=2, sticky="EW")
        self.myList = Listbox(self,width=30, height=10, font=self.listfont)
        self.myList.grid(row=3, column=0)

        mainloop()

    def addItem(self):
        self.myList.insert(END, self.newName.get().ljust(15,".") + " : " + self.newScore.get())

if __name__ == "__main__":
    app = App()
