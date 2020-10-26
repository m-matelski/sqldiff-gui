
from tkinter import *

root = Tk()

def hello():
        print("hello!")

def popup(event):
        menu.post(event.x_root, event.y_root)
        menu.focus_set()

def popupFocusOut(self,event=None):
        menu.unpost()

# create a canvas
frame = Frame(root, width=512, height=512)
frame.pack()

# create a popup menu
menu = Menu(frame, tearoff=0)
menu.add_command(label="Undo", command=hello)
menu.add_command(label="Redo", command=hello)
menu.bind("<FocusOut>",popupFocusOut)

# attach popup to canvas
frame.bind("<Button-3>", popup)

mainloop()