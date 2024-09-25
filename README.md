# A Tkinter Database with multiple frames

This project has been created with two purposes:

1. To show you one way of making a tkinter file with multiple "screens" using one window.
2. To show you how to connect to a database and create on-screen forms that interact with stored data.

I will soon make a video explaining these, but for now these are some things to note:
This project consists of 5 screens, which allow users to log in, view and edit users and create links between two database tables (in this example, we are registering People to different Activities, using a simple 3-table relational database)
The file main.py creates the main window of the app. It doesn't contain any of the actual screen controls.

Each screen is created as a separate python file (menu.py, login.py, peopleform.py etc)
The main.py file imports these.

Switching between screens is done as follows:

A list is made in the main app which contains each of the different imported screens. Each one is a Frame object:

        self.frames = [ LoginFrame(self), MenuFrame(self),
                        PeopleFormFrame(self), PeopleListFrame(self),
                        JoiningFrame(self)]

When this happens, the frames are instantly created, but not shown. This is important to note, as will become apparent later.

In order to switch frames, the main.py file has a method switchFrame

    def switchFrame(self, frameNum):
        # hide all frames except the one chosen
        for i in range(len(self.frames)):
            frame = self.frames[i]
            if i == frameNum:
                frame.grid(row=0, column=0, sticky="NSWE")
                frame.loadUp()
            else:
                frame.grid_forget()
                
This method takes a parameter framenum, which relates to the number of the frame in the list shown above (0 is login, 1 is menu etc)
The method hides all other frames (using grid_forget) and shows the desired frame.
It also triggers the loadUp() method of the desired frame. More on this later.

### Some other things to note about main.py

This file is a demo, so it features a method that creates the database from scratch every time, and fills it with some sample data.
Because of this, it might appear that any changes made to the database are not saved. They are saved, but they are also destroyed every time you reload the program. This is just for test purposes, so you obviously wouldn't do this in your final project.

The main.py file needs to contain attributes that all the frames might need to access. In this demo, the only ones worth mentioning are self.db which is a connection to the database file, and self.loggedin, which is a record of the username of the person who logged in. Different screens might need to know who the curent user is.

## Making a frame

A good example to look at is peopleform.py

A typical frame is a class of type tk.Frame. It has an init method which sets up the controls on the form (the labels, text boxes, buttons etc)
####The init section does not perform any database access, or try putting data into the textboxes.
This is because it is created as soon as the program runs, before anyone has logged in, and before we have even connected to the database.

Instead, we use a method called loadUp() which is run when the frame first appears on the screen
