import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        tk.Frame.__init__(self,parent)
        TitleLabel = tk.Label(self,text="Welcome to the Activities Database")
        TitleLabel.grid(row=0, column=0, columnspan=3, sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))
        loggedin = tk.StringVar()
        loggedin.set(parent.loggedInUser)
        self.usernameLabel = tk.Label(self,text = "Logged in as" + loggedin.get(), font=("Arial",8), fg="blue")
        self.usernameLabel.grid(row=10,column=2,sticky="E")

        # space out row 1
        self.rowconfigure(1,minsize=50)

        b1 = tk.Button(self,text="View/Edit People", command=lambda: parent.switchFrame(2))
        b1.grid(row=2,column = 0)
        
        # space out row 3
        self.rowconfigure(3,minsize=50)

        b2 = tk.Button(self,text="Link people to activities", command=lambda: parent.switchFrame(4))
        b2.grid(row=4,column = 0)

        self.columnconfigure(0, weight=1)

    def loadUp(self):
        self.usernameLabel.config(text="Logged in as: " + self.parent.loggedInUser)

