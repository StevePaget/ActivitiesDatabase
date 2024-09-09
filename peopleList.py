import tkinter as tk
from tkinter import messagebox

class PeopleListFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        self.data = []
        self.databoxes = []

        tk.Frame.__init__(self, parent)
        back = tk.Button(self, text="Main Menu", command=lambda: self.parent.switchFrame(1))
        back.grid(row=0, column=0, sticky="W")
        self.rowconfigure(1,minsize=20)
        self.columnconfigure(1, weight=1)

        TitleLabel = tk.Label(self, text="View or Edit People - List View")
        TitleLabel.grid(row=2, column=0, columnspan=3, sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))

        formView = tk.Button(self, text="Form View", command = lambda: self.parent.switchFrame(2))
        formView.grid(row=0,column=2, sticky="E")
        self.datagrid = tk.Frame(self)
        self.datagrid.grid(row=4,column=0,sticky="NSEW",columnspan=3)
        self.delbtn = tk.Button(self, text="Del", command=self.deleteChecked)
        self.delbtn.grid(row=5, column=2, sticky="E")
        self.columnconfigure(2,weight=1)

        saveBtn = tk.Button(self,text="Save Changes", command = self.saveData)
        saveBtn.grid(row=5, column=1, sticky="E")

    def saveData(self):
        for row in self.databoxes:
            c = self.db.cursor()
            c.execute("UPDATE tblPeople  SET FirstName = ?, Surname = ?, Form = ? WHERE personID = ?",
                               [row[1][0].get(),row[2][0].get(),row[3][0].get(),row[0][0].get()] )
            self.db.commit()

    def updateDatagrid(self):
        #clear the old grid
        for row in self.databoxes:
            for item in row:
                item[1].destroy()
        self.databoxes=[]
        for rownum in range(len(self.data)):
            self.databoxes.append([])
            for fieldNum in range(len(self.data[rownum])):
                self.databoxes[-1].append([tk.StringVar()])
                self.databoxes[-1][-1][0].set(str(self.data[rownum][fieldNum]))
                self.databoxes[-1][-1].append(tk.Entry(self.datagrid, textvariable=self.databoxes[-1][-1][0]))
                self.databoxes[-1][-1][1].grid(row=rownum, column=fieldNum, padx=5, pady=2)
            self.databoxes[-1][0][1].config(state="disabled") # This makes this column read only
            self.databoxes[-1].append([tk.IntVar()])
            self.databoxes[-1][-1].append(tk.Checkbutton(self.datagrid, variable=self.databoxes[-1][-1][0]))
            self.databoxes[-1][-1][1].grid(row=rownum, column=fieldNum+1,padx=5)


    def refreshData(self):
        c = self.db.cursor()
        result = c.execute("SELECT personID, firstName, surname, form from tblPeople")
        self.data = result.fetchall()

    def deleteChecked(self):
        numChecked = 0
        c = self.db.cursor()
        for row in self.databoxes:
            if row[-1][0].get()==1:
                numChecked+=1
        if numChecked>0:
            OK = messagebox.askokcancel("Warning", str(numChecked) + " row(s) to delete.\nAre you sure?")
            if OK:
                for row in self.databoxes:
                    if row[-1][0].get() == 1:
                        print("deleting", row[0][0].get(), row[1][0].get())
                        c.execute("DELETE FROM tblPeople WHERE personID = ?", [row[0][0].get()])
                        self.db.commit()
        self.refreshData()
        self.updateDatagrid()

    def loadUp(self):
        print("loaded People List")
        self.refreshData()
        self.updateDatagrid()