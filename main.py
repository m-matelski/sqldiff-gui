from gui.sqldiff_window import SqlCompareDualTextWindow
import tkinter as tk

if __name__ == '__main__':
    mw = SqlCompareDualTextWindow()
    mw.title('Sql Diff')
    #mw.attributes('-zoomed', True)
    # mw.mainloop()
    tk.mainloop()