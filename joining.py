import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

class JoiningFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        tk.Frame.__init__(self, parent)
        back = tk.Button(self, text="Main Menu", command = lambda: self.parent.switchFrame(1))
        back.grid(row=0,column=0, sticky="W")

        self.titlefont = tkFont.Font(family="Arial", size=20, slant="italic")
        self.buttonfont = tkFont.Font(family="Arial", size=18)
        self.listfont = tkFont.Font(family="Consolas", size=18)

        l1 = tk.Label(self, text="People", font=self.listfont)
        l1.grid(row=1, column=0, sticky="NSWE")
        self.peopleList = tk.Listbox(self,width=20, height=10, font=self.listfont)
        self.peopleList.grid(row=2, column=0, rowspan = 3)

        l2 = tk.Label(self, text="Activities", font=self.listfont)
        l2.grid(row=1, column=2, sticky="NSWE")
        self.activityList = tk.Listbox(self,width=20, height=10, font=self.listfont)
        self.activityList.grid(row=2, column=2, rowspan = 3)
        self.columnconfigure(1,minsize=100)



    def saveData(self):
        self.refreshData()

    def refreshData(self):
        c = self.parent.db.cursor()
        # populate the People list box:
        r = c.execute("SELECT * from tblPeople")
        self.peopleData = r.fetchall()
        for i in range(len(self.peopleData)):
            rowtext = "{} {} {}".format((self.peopleData[i][0], self.peopleData[i][2],self.peopleData[i][3]))
            self.peopleList.insert("END", rowtext )


        r = c.execute("SELECT p.firstName, p.surname, p.form, a.activityName, a.day from tblPeople p, tblJoining j, tblActivities a WHERE p.personID = j.personID and a.activityID = j.ActivityID")
        self.data = r.fetchall()
        # now fill the boxes
        


    def loadUp(self):
        print("loaded Joining")
        self.refreshData()