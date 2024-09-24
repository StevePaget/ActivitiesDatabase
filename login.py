import tkinter as tk

class LoginFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
        tk.Frame.__init__(self, parent)

        self.parent.bind("<Return>", self.keypressed)
        TitleLabel = tk.Label(self, text="Welcome to the Activities Database")
        TitleLabel.grid(row=0, column=0, columnspan=3, sticky="NSWE")
        TitleLabel.config(font=("Arial", 24))

        spacer1 = tk.Label(self, text=" ")
        spacer1.grid(row=1, column=0)
        l1 = tk.Label(self,text="Username", font=("Arial", 12))
        l1.grid(row=2, column=0)
        self.unamebox = tk.Entry(self,width=20, font=("Arial", 12))
        self.unamebox.grid(row=2,column=1)

        spacer2 = tk.Label(self, text=" ")
        spacer2.grid(row=3, column=0)
        l2 = tk.Label(self,text="Password", font=("Arial", 12))
        l2.grid(row=4, column=0)
        self.passbox = tk.Entry(self,width=20, show="*", font=("Arial", 12))
        self.passbox.grid(row=4,column=1 )


        spacer3 = tk.Label(self, text=" ")
        spacer3.grid(row=5, column=0)
        b2 = tk.Button(self, text="Submit", command=self.loginSubmitted)
        b2.grid(row=6, column=0)
        spacer4 = tk.Label(self, text=" ")
        spacer4.grid(row=7, column=0)

        self.feedbacklabel = tk.Label(self, "", foreground="red")
        self.feedbacklabel.grid(row=8, column=0)
        self.columnconfigure(2, weight=1)

    def keypressed(self,event):
        # they pressed return. have they entered a username yet?
        if len(self.unamebox.get())>0:
            self.loginSubmitted()

    def loadUp(self):
        print("loaded Login")
        # print("Bypassed login")
        # self.controller.successfulLogin("asmith")

    def loginSubmitted(self):
        c = self.parent.db.cursor()
        r = c.execute("SELECT * from tblPeople WHERE username = ? and password = ?", [self.unamebox.get(), self.passbox.get()])
        results = r.fetchall()
        if len(results)>0:
        #if True:
            self.feedbacklabel.config(text="")
            self.parent.successfulLogin(self.unamebox.get())
            return True
        else:
            self.feedbacklabel.config(text="Incorrect Login")
            return False
