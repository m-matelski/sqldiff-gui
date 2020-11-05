import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror

import psycopg2
import sqldiff as sqldiff
import teradatasql

from appdata.connections import read_connection_data
from gui.sqlpanelin import SqlInputPanel


class SqlCompareDualTextWindow(tk.Tk):
    """
    Custom Widget with two custom SqlPanels sside by side
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

        # Creating Top panel
        self.top_frame = tk.Frame(self)

        # top buttons
        self.btn_compare = ttk.Button(self.top_frame, text='Compare', command=self.compare)
        self.btn_compare.grid(column=0, row=0, sticky='w')


        # Creating sql panels in main Frame
        self.sql_panel_source = SqlInputPanel(self, padx=5, pady=2)
        self.sql_panel_target = SqlInputPanel(self, padx=5, pady=2)

        # Middle frame spacing vertically Sql input panels
        self.frame_middle = tk.Frame(self)

        # Optional buttons for middle frame
        self.ic = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/switch.png'))
        self.ic2 = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/database.png'))
        self.btn_1 = tk.Button(self.frame_middle, image=self.ic)

        # Spacing two panels and space frame in three grid columns
        self.top_frame.grid(column=0, columnspan=3, row=0, sticky='nwes', padx=4, pady=4)
        self.sql_panel_source.grid(column=0, row=1, sticky='nwes')
        self.sql_panel_target.grid(column=2, row=1, sticky='nwes')
        self.frame_middle.grid(column=1, row=1, sticky='')

        # Optional components (such as buttons) in middle frame
        self.btn_1.grid(column=0, row= 0, sticky='') # button in

        # Setting Widgets weight
        self.grid_rowconfigure(1, weight=1) # weight not initialized so set to 1
        self.grid_columnconfigure(0, weight=10000) # Big weight differences causes that middle frame is static
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=10000)

        # self.frame_middle.grid_rowconfigure(0, weight=1)
        # self.frame_middle.grid_columnconfigure(0, weight=1)
        self.connection_data = None
        self.refresh_connections()

    def refresh_connections(self):
        self.connection_data = read_connection_data()
        connections = list(self.connection_data.keys())
        self.sql_panel_source.combo_connection['values'] = connections
        self.sql_panel_target.combo_connection['values'] = connections

    def compare(self):
        src_con = self.connection_data.get(self.sql_panel_source.combo_connection.get(), None)
        tgt_con = self.connection_data.get(self.sql_panel_target.combo_connection.get(), None)
        if not src_con:
            showerror('W', 'Invalid source connection!')
            return
        if not tgt_con:
            showerror('W', 'Invalid target connection!')
            return

        src_query = self.sql_panel_source.sql_text.get_text()
        tgt_query = self.sql_panel_target.sql_text.get_text()

        # TODO some kind of dbtype mapping to conenction object
        # with psycopg2.connect(**connection_params_postgres) as postgres_connection, \
        #         teradatasql.connect(**connection_params_teradata) as teradata_connection:
        #
        #     result = sqldiff.compare(
        #         source_connection=teradata_connection,
        #         source_query=src_query,
        #         target_connection=postgres_connection,
        #         target_query=tgt_query)