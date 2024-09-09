import tkinter as tk
from tkinter import messagebox

class PeopleFormFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.recNum = 0

        tk.Frame.__init__(self, parent)
        self.columnconfigure(1,weight=1)
        back = tk.Button(self, text="Main Menu", command = lambda: self.parent.switchFrame(1))
        back.grid(row=0,column=0, sticky="W")

        listView = tk.Button(self, text="List View", command = lambda: self.parent.switchFrame(3))
        listView.grid(row=0,column=2, sticky="E")
        self.rowconfigure(1,minsize=20)
        TitleLabel = tk.Label(self, text="View or Edit People - Form View")
        TitleLabel.grid(row=2, column=0, columnspan=3,sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))

        self.rowconfigure(3, minsize=30)
        ul = tk.Label(self, text="ID:")
        ul.grid(row=4, column=0)
        self.ID = tk.StringVar()
        self.IDBox = tk.Label(self, textvariable = self.ID)
        self.IDBox.grid(row=4, column=1)

        self.IDFeedback = tk.Label(self, text="", fg="red")
        self.IDFeedback.grid(row=4, column=2)

        fn = tk.Label(self, text="First name:")
        fn.grid(row=5, column=0)
        self.firstname = tk.StringVar()
        self.firstnameBox = tk.Entry(self, textvariable = self.firstname)
        self.firstnameBox.grid(row=5, column=1)

        sn = tk.Label(self, text="Surname:")
        sn.grid(row=6, column=0)
        self.surname = tk.StringVar()
        self.surnameBox = tk.Entry(self, textvariable = self.surname)
        self.surnameBox.grid(row=6, column=1)

        fm = tk.Label(self, text="Form Group:")
        fm.grid(row=7, column=0)
        self.form = tk.StringVar()
        self.formBox = tk.Entry(self, textvariable = self.form)
        self.formBox.grid(row=7, column=1)
        self.rowconfigure(8,minsize=50)
        bottomButtons = tk.Frame(self)
        bottomButtons.grid(row=9,column=0, columnspan=2, sticky="NSEW")
        prevBtn = tk.Button(bottomButtons, text="<< Previous", command = lambda: self.changeRec(-1))
        prevBtn.grid(row=0,column=0)

        nextBtn = tk.Button(bottomButtons, text="Next >>", command=lambda: self.changeRec(1))
        nextBtn.grid(row=0, column=4)

        self.newBtn = tk.Button(bottomButtons, text="Create New", command=self.newPerson)
        self.newBtn.grid(row=0, column=1)

        self.delBtn = tk.Button(bottomButtons, text="Delete", command=self.delete)
        self.delBtn.grid(row=0, column=3)

        saveBtn = tk.Button(bottomButtons, text="Save Changes", command=self.saveData)
        saveBtn.grid(row=0, column=2)

        bottomButtons.columnconfigure(0,weight=1)
        bottomButtons.columnconfigure(1,weight= 1)
        bottomButtons.columnconfigure(2, weight=1)
        bottomButtons.columnconfigure(3, weight=1)
        bottomButtons.columnconfigure(4, weight=1)

    def saveData(self):
        if self.recNum == -1:
            # this is a new person
            self.IDFeedback.config(text="")
            c=self.parent.db.cursor()
            c.execute("INSERT INTO tblPeople (personID, firstName, surname, form) VALUES (NULL,?,?,?)", [self.ID.get(), self.firstname.get(), self.surname.get(), self.form.get()])
            self.recNum = len(self.data)
            self.refreshData()

        else:
            c=self.parent.db.cursor()
            c.execute("UPDATE tblPeople SET personID = ?, firstName = ?, surname = ?, form = ? WHERE personID = ?",
                               [self.ID.get(), self.firstname.get(), self.surname.get(), self.form.get(), self.data[self.recNum][0]])
            self.parent.db.commit()
        self.refreshData()


    def newPerson(self):
        self.recNum = -1
        self.ID.set("")
        self.firstname.set("")
        self.surname.set("")
        self.form.set("")
        self.IDBox.focus()

    def delete(self):
        OK = messagebox.askokcancel("Warning", "Are you sure you want to delete this?")
        if OK:
            c=self.parent.db.cursor()
            c.execute("DELETE from tblPeople where personID = ?", [self.ID.get()])
            self.parent.db.commit()
            self.recNum = 0
            self.refreshData()


    def changeRec(self, val):
        self.recNum = (self.recNum + val) % len(self.data)
        if self.recNum<0:
            self.recNum = 0
        self.refreshData()

    def changeUserDisplayed(self):
        self.ID.set(self.data[self.recNum][0])
        self.firstname.set(self.data[self.recNum][2])
        self.surname.set(self.data[self.recNum][3])
        self.form.set(self.data[self.recNum][4])
        print("updated")

    def refreshData(self):
        c = self.parent.db.cursor()
        r = c.execute("SELECT * from tblPeople")
        self.data = r.fetchall()
        self.changeUserDisplayed()

    def loadUp(self):
        print("loaded People")
        self.refreshData()