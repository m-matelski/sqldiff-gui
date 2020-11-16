import os

from appdata.pyinstaller_data import resource_path
from gui.sqldiff_window import SqlCompareDualTextWindow
import tkinter as tk

if __name__ == '__main__':
    mw = SqlCompareDualTextWindow()
    mw.title('Sql Diff')
    # mw.attributes('-zoomed', True)
    # mw.attributes('-fullscreen', True)
    # fullscreen on windows
    mw.wm_state('zoomed')
    # mw.mainloop()
    # mw.iconbitmap(os.path.join('gui/resources/icons/sql_diff_icon.ico'))
    # mw.iconbitmap(os.path.join('gui/resources/icons/32x32/switch.png'))
    # imgicon = tk.PhotoImage(file=os.path.join('gui/resources/icons/32x32/switch.png'))

    # TODO - manage image files for pyinstaller
    # Icon works on windows
    # imgicon = tk.PhotoImage(file=os.path.join('gui/resources/icons/sql_diff_icon.png'))
    # mw.tk.call('wm', 'iconphoto', mw._w, imgicon)

    # sql_diff_icon.png
    imgicon = tk.PhotoImage(file=resource_path('sql_diff_icon.png'))
    mw.tk.call('wm', 'iconphoto', mw._w, imgicon)

    mw.mainloop()
