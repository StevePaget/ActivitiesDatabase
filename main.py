import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql
from login import LoginFrame
from menu import MenuFrame
from peopleForm import PeopleFormFrame
from peopleList import PeopleListFrame
from joining import JoiningFrame

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x600")
        self.title("Main Menu")
        self.loggedInUser = ""
        self.db = sql.connect("demoFile.sqlite")

        self.frames = [ LoginFrame(self), MenuFrame(self),
                        PeopleFormFrame(self), PeopleListFrame(self),
                        JoiningFrame(self)]

        self.switchFrame(0)

    def successfulLogin(self,username):
        self.loggedInUser = username
        print("Logged in as", username)
        self.switchFrame(1)


    def switchFrame(self, frameNum):
        # hide all frames except the one chosen
        for i in range(len(self.frames)):
            frame = self.frames[i]
            if i == frameNum:
                frame.grid(row=0, column=0, sticky="NSWE")
                frame.loadUp()
            else:
                frame.grid_forget()


def createDemoData():
    db = sql.connect("demoFile.sqlite")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS tblPeople")
    c.execute("CREATE TABLE tblPeople (personID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, firstName TEXT, surname TEXT, form TEXT, password TEXT, userLevel INT)")
    c.execute("INSERT INTO tblPeople VALUES (NULL,?,?,?,?,?,?)", ['snallon','Steve', 'Nallon', '7SAP','maggie',0])
    c.execute("INSERT INTO tblPeople VALUES (NULL,?,?,?,?,?,?)", ['myarwood','Mike', 'Yarwood', '8JML','bob',0])
    c.execute("INSERT INTO tblPeople VALUES (NULL,?,?,?,?,?,?)", ['jculshaw','Jon', 'Culshaw', '8JML',"frank",0])
    c.execute("INSERT INTO tblPeople VALUES (NULL,?,?,?,?,?,?)", ['rbremner','Rory', 'Bremner', '7SAP',"paddy",0])
    c.execute("INSERT INTO tblPeople VALUES (NULL,?,?,?,?,?,?)", ['scoogan','Steve', 'Coogan', '7SAP',"alan",1])
    c.execute("DROP TABLE IF EXISTS tblActivities")
    c.execute("CREATE TABLE tblActivities (activityID INTEGER PRIMARY KEY AUTOINCREMENT, activityname TEXT, day INT)")
    c.execute("INSERT INTO tblActivities VALUES (NULL,?,?)", ["Badminton", 1])
    c.execute("INSERT INTO tblActivities VALUES (NULL,?,?)", ["Cricket", 1])
    c.execute("INSERT INTO tblActivities VALUES (NULL,?,?)", ["Tennis", 3])
    c.execute("INSERT INTO tblActivities VALUES (NULL,?,?)", ["Knitting", 3])
    c.execute("INSERT INTO tblActivities VALUES (NULL,?,?)", ["Board Games", 2])
    c.execute("INSERT INTO tblActivities VALUES (NULL,?,?)", ["Dog Training", 4])
    c.execute("DROP TABLE IF EXISTS tblJoining")
    c.execute("CREATE TABLE tblJoining (joiningID INTEGER PRIMARY KEY AUTOINCREMENT, personID INT, activityID INT)")
    c.execute("INSERT INTO tblJoining VALUES (NULL,?,?)", [1,2])
    c.execute("INSERT INTO tblJoining VALUES (NULL,?,?)", [1,4])
    c.execute("INSERT INTO tblJoining VALUES (NULL,?,?)", [2,1])
    c.execute("INSERT INTO tblJoining VALUES (NULL,?,?)", [2,2])
    db.commit()

    r = c.execute("SELECT * FROM tblPeople")
    results = r.fetchall()
    print(results)
    r = c.execute("SELECT * FROM tblActivities")
    results = r.fetchall()
    print(results)


createDemoData()
app = Main()
app.mainloop()