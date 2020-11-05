import os
from tkinter import ttk

import tkinter as tk

from gui.connection_manager import ConnectionManagerWindow
from gui.sqltextin import SqlText


class SqlInputPanel(tk.Frame):
    """
    Custom widget representing SqlText Widget with navigation bar.
    """
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.config(highlightbackground='#999999')
        self.config(highlightthickness=1)

        # Top frame for inputs, located above SqlText Widget
        self.top_frame = tk.Frame(self, bd=0, relief='solid')

        # Two Frames inside top_frame alligned to left aright
        self.top_left_frame = tk.Frame(self.top_frame, bd=0, relief='solid')
        self.top_right_frame = tk.Frame(self.top_frame, bd=0, relief='solid')

        # # Adding buttons to top left frame
        # self.ic = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/format_text.png'))
        # self.ic2 = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/database.png'))
        # self.btn_1 = ttk.Button(self.top_left_frame, image= self.ic)
        # self.btn_2 = ttk.Button(self.top_left_frame, image= self.ic2)
        # #self.btn_3 = ttk.Button(self.top_left_frame, image= self.ic)
        # self.btn_3 = ttk.Button(self.top_left_frame, text='asd')
        # # Setting position of top left components
        # self.btn_1.grid(row=0, column=0, sticky='', ipady=0, ipadx=0)
        # self.btn_2.grid(row=0, column=1, sticky='')
        # self.btn_3.grid(row=0, column=2, sticky='')

        # Adding buttons to top left frame
        self.ic_add_connection = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/add_connection.png'))
        self.btn_add_connection = ttk.Button(self.top_right_frame, image= self.ic_add_connection, command=self.open_connection_manager)
        self.combo_connection = ttk.Combobox(self.top_right_frame, state='readonly', values=['Postgres1', 'connection2'])
        self.combo_connection.bind('<<ComboboxSelected>>', self.combo_connection_clear_selection)

        self.sql_text = SqlText(self, height=30, width=10)

        # Positioning using Grid System
        self.top_frame.grid(column=0, row=0, sticky='nwes')
        self.top_left_frame.grid(column=0, row=0, sticky='w')
        self.top_right_frame.grid(column=1, row=0, sticky='e')
        self.sql_text.grid(column=0, row=1, sticky='nwes')

        # Setg position of top right bar components
        self.combo_connection.grid(column=1, row=0, sticky='', padx=2, pady=2)
        self.btn_add_connection.grid(column=0, row=0, padx=2, pady=2)

        # Setting weights - such a big difference allow to keep top bar in constant size while SqlText is scaling
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=400000)
        self.grid_columnconfigure(0, weight=1)

        # Setting weights of top bar, splitting bar on half to left and right sides
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # Weights for top right icons
        self.top_right_frame.grid_rowconfigure(0, weight=1)
        self.top_right_frame.grid_columnconfigure(0, weight=1)

        # Weights for top left icons
        self.top_left_frame.grid_rowconfigure(0, weight=1)
        self.top_left_frame.grid_columnconfigure(0, weight=1)
        self.top_left_frame.grid_columnconfigure(1, weight=1)
        self.top_left_frame.grid_columnconfigure(2, weight=1)

    def combo_connection_clear_selection(self, event=None):
        self.combo_connection.selection_clear()

    def open_connection_manager(self):
        cm = ConnectionManagerWindow()

        # window_height = 400
        # window_width = 700
        #
        # win_x = self.winfo_x()
        # win_y = self.winfo_y()
        #
        #
        # x_cordinate = int(self.winfo_x() + (self.winfo_width()/2))
        # y_cordinate = int(self.winfo_y() + (self.winfo_height()/2))
        #
        # # x_cordinate = 100
        # # y_cordinate = 100
        #
        # cm.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        cm.grab_set()