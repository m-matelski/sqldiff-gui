from tkinter import ttk

import tkinter as tk

from sqldiff import ColumnsComparisonResult

from gui.sqlpanelin import SqlInputPanel

# ColumnsComparisonResult
from gui.sqltextin import SqlText


class SqlDiffResult(tk.Toplevel):

    def __init__(self, comparison_result: ColumnsComparisonResult, *args, **kwargs):
        # Window
        super().__init__(*args, **kwargs)

        self.comparison_result = comparison_result

        self.sql_text_source = SqlText(self, padx=5, pady=2, wrap='none')
        self.sql_text_target = SqlText(self, padx=5, pady=2, wrap='none')
        self.sql_text_source.on_xscrollcommand = self.on_xscrollcommand_source
        self.sql_text_source.on_yscrollcommand = self.on_yscrollcommand_source
        self.sql_text_target.on_xscrollcommand = self.on_xscrollcommand_target
        self.sql_text_target.on_yscrollcommand = self.on_yscrollcommand_target

        self.sql_text_source.grid(column=0, row=0, sticky='nwes')
        self.sql_text_target.grid(column=1, row=0, sticky='nwes')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.load_comparison_result()
        self.disable_sql_text()

    def load_comparison_result(self):
        for i in range(100):
            self.sql_text_source.insert(tk.END, f"field{i} DECIMAL(15,5)\n")
            self.sql_text_target.insert(tk.END, f"field{i} DECIMAL(15,5)\n")
        pass

    def disable_sql_text(self):
        for i in (self.sql_text_source, self.sql_text_target):
            i.put_styled_text()
            i.configure(state='disabled')

    def on_yscrollcommand_source(self, first, last):
        print(f'on_yscrollcommand ({first}, {last})')
        if not self.has_text_scrollbars_the_same_position():
            view_pos = self.sql_text_source.yview()
            self.sql_text_target.yview_moveto(view_pos[0])

    def on_xscrollcommand_source(self, first, last):
        if not self.has_text_scrollbars_the_same_position():
            view_pos = self.sql_text_source.xview()
            self.sql_text_target.xview_moveto(view_pos[0])

    def on_yscrollcommand_target(self, first, last):
        if not self.has_text_scrollbars_the_same_position():
            view_pos = self.sql_text_target.yview()
            self.sql_text_source.yview_moveto(view_pos[0])

    def on_xscrollcommand_target(self, first, last):
        print(f'on_xscrollcommand ({first}, {last})')
        if not self.has_text_scrollbars_the_same_position():
            view_pos = self.sql_text_target.xview()
            self.sql_text_source.xview_moveto(view_pos[0])

    def has_text_scrollbars_the_same_position(self):
        return self.sql_text_source.hbar.get() == self.sql_text_target.hbar.get() and \
               self.sql_text_source.vbar.get() == self.sql_text_target.vbar.get()
