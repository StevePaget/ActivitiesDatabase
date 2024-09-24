import tkinter as tk
from tkinter import ttk
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

        # person select combobox
        l1 = tk.Label(self, text="Choose a person", font = self.titlefont)
        l1.grid(row=2, column=0)
        self.personCombo = ttk.Combobox(self, font=self.listfont)
        self.personCombo.grid(row=3, column=0)
        self.personCombo.bind("<<ComboboxSelected>>", self.personChosen)
        self.selectedpersonid = None

        self.columnconfigure(1,minsize=100)
        # list of current activities
        l2 = tk.Label(self, text="Joined activities", font = self.titlefont)
        l2.grid(row=2, column=2, sticky="NW")
        self.joinedlist = tk.Listbox(self,height=10, width=30, font = self.listfont)
        self.joinedlist.grid(row=3, column = 2, rowspan=3, sticky="NW")

        # box for adding new activities
        l3 = tk.Label(self,text="Choose a new activity to add:", font=self.buttonfont)
        l3.grid(row=7, column=2, sticky="NW")
        self.newactivitycombo = ttk.Combobox(self, font=self.listfont)
        self.newactivitycombo.grid(row=8, column=2, sticky="NW")
        addButton = tk.Button(self,text="Add", command=self.addjoin)
        addButton.grid(row=8, column=3, sticky = "NW")

    def refreshData(self):
        c = self.parent.db.cursor()
        # populate the People combo box:
        r = c.execute("SELECT * from tblPeople")
        self.peopleData = r.fetchall()
        people = []
        for i in range(len(self.peopleData)):
            rowtext = "{} {} {}".format(self.peopleData[i][0], self.peopleData[i][2],self.peopleData[i][3])
            people.append(rowtext)
        self.personCombo['values'] = people
        # grab all activities
        r = c.execute("SELECT * from tblActivities")
        self.activityData = r.fetchall()
        self.activities = []
        for i in range(len(self.activityData)):
            self.activities.append(self.activityData[i][1])
        self.newactivitycombo['values'] = self.activities

    def addjoin(self):
        if not self.selectedpersonid:
            return  # no one selected yet
        
        # add this activity to this person's list, so long as it's not already there
        selectedrow = self.newactivitycombo.current()
        selectedactivity = self.activityData[selectedrow]
        print("adding",selectedactivity[1])
        if selectedactivity[1] in self.joinedactivities:
            print("already there")
        else:
            # add it to the database
            c = self.parent.db.cursor()
            c.execute("INSERT INTO tblJoining Values (NULL, ?,?)",(self.selectedpersonid,selectedactivity[0]))
            self.parent.db.commit()
            # call the function that loads the data
            # into the joined list
            self.personChosen(None)

    def personChosen(self, e):
        # put the list of activities this person has joined in the
        # list box
        # identify selected person
        selectedrow = self.personCombo.current()
        person = self.peopleData[selectedrow]
        self.selectedpersonid = person[0]
        c = self.parent.db.cursor()
        r = c.execute("SELECT a.activityname from tblActivities a, tblJoining j WHERE j.activityID = a.activityID and j.personID = ?",(self.selectedpersonid,))
        self.joinedactivities = [row[0] for row in r.fetchall()]
        self.joinedlist.delete(0,tk.END)
        for activity in self.joinedactivities:
            self.joinedlist.insert(tk.END,activity)

    def loadUp(self):
        print("loaded Joining")
        self.refreshData()