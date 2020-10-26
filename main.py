import tkinter as tk

# Label, Button, Entry (single line), Text, Frame (box for other widgets)
# it uses text units for width and height measurements, tahts why 10x10 is not a square
from tkinter import N, S, E, W

from gui.custom_widgets import SqlText, SqlInputPanel, SqlCompareDualInputPanel

root = tk.Tk()
root.option_add('*tearOff', tk.FALSE)

def donothing():
    pass

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)








content = tk.Frame(root)



sql_compare_dual_panel = SqlCompareDualInputPanel(content, relief='solid', padx=5, pady=5)

content.grid(column=0, row=0, sticky=(N, S, E, W))
sql_compare_dual_panel.grid(column=0, row=0, sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)


root.mainloop()

