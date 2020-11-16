from tkinter import ttk

import tkinter as tk

from sqldiff import ColumnsComparisonResult, KeyColumnComparisonResult

from gui.sqlpanelin import SqlInputPanel

# ColumnsComparisonResult
from gui.sqltextin import SqlText


class SqlDiffResult(tk.Toplevel):

    TAG_DIFF_MATCH = 'TAG_DIFF_MATCH'
    TAG_DIFF_ORDER_DONT_MATCH = 'TAG_DIFF_ORDER_DONT_MATCH'
    TAG_DIFF_TYPE_DONT_MATCH = 'TAG_DIFF_TYPE_DONT_MATCH'
    TAG_DIFF_NO_MATCH_AND_ORDER = 'TAG_DIFF_NO_MATCH_AND_ORDER'
    TAG_DIFF_TYPE_DONT_EXIST = 'TAG_DIFF_TYPE_DONT_EXIST'

    DIFF_MODE_BOTH = 'Source/Target'
    DIFF_MODE_SOURCE = 'Source'
    DIFF_MODE_TARGET = 'Target'
    DIFF_MODES = (DIFF_MODE_BOTH, DIFF_MODE_SOURCE, DIFF_MODE_TARGET)


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

        for sql_text in (self.sql_text_source, self.sql_text_target):
            sql_text.tag_config(self.TAG_DIFF_MATCH, background="#adffc3")
            sql_text.tag_config(self.TAG_DIFF_ORDER_DONT_MATCH, background="#abe7ff")
            sql_text.tag_config(self.TAG_DIFF_TYPE_DONT_MATCH, background="#fffbc4")
            sql_text.tag_config(self.TAG_DIFF_NO_MATCH_AND_ORDER, background="#ffb7dd")
            sql_text.tag_config(self.TAG_DIFF_TYPE_DONT_EXIST, background="#ff9a9a")

        self.frame_top = tk.Frame(self)
        self.frame_top.grid(column=0, row=0, sticky='', columnspan=2, padx=3, pady=3)
        # self.frame_top.config(bd=1, relief=tk.SOLID)
        self.frame_top.grid_columnconfigure(0, weight=1)
        self.frame_top.grid_columnconfigure(1, weight=1)
        self.frame_top.grid_rowconfigure(0, weight=1)

        self.lbl_diff_mode = tk.Label(self.frame_top, text='Diff mode:')
        self.lbl_diff_mode.grid(column=0, row=0, sticky='nw', padx=5)

        self.combo_diff_mode = ttk.Combobox(self.frame_top)
        self.combo_diff_mode['values'] = self.DIFF_MODES
        self.combo_diff_mode.state(['readonly'])
        self.combo_diff_mode.bind('<<ComboboxSelected>>', self.diff_mode_selection)
        self.combo_diff_mode.grid(column=1, row=0, sticky='nw')
        self.combo_diff_mode.current(0)

        self.sql_text_source.grid(column=0, row=1, sticky='nwes')
        self.sql_text_target.grid(column=1, row=1, sticky='nwes')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=10000)
        self.grid_rowconfigure(0, weight=1)

        self.load_comparison_result()

    def diff_mode_selection(self, event=None):
        self.combo_diff_mode.selection_clear()
        self.load_comparison_result()

    def load_comparison_result(self):

        self.set_sql_text_state('normal')
        self.sql_text_clear()
        diff_mode = self.combo_diff_mode.get()


        comparison_result = self.comparison_result
        if diff_mode==self.DIFF_MODE_SOURCE:
            comparison_result = self.comparison_result.order_by_source()
        elif diff_mode==self.DIFF_MODE_TARGET:
            comparison_result = self.comparison_result.order_by_target()

        # print(self.comparison_result)
        # for i in range(100):
        #     self.sql_text_source.insert(tk.END, f"field{i} DECIMAL(15,5)\n")
        #     self.sql_text_target.insert(tk.END, f"field{i} DECIMAL(15,5)\n")
        for cr in comparison_result:
            src_verse = (str(cr.key.source) if cr.key.source else '') + '\n'
            tgt_verse = (str(cr.key.target) if cr.key.target else '') + '\n'
            self.sql_text_source.insert('end', src_verse)
            self.sql_text_target.insert('end', tgt_verse)

        for i in (self.sql_text_source, self.sql_text_target):
            i.put_styled_text()

        # set backgrounds
        # self.sql_text_source.tag_add('warning', '1.2', '5.0')
        for i, cr in enumerate(comparison_result, start=1):
            start = str(i) + '.0'
            end = str(i+1) + '.0'
            tag = self.get_tag(cr)
            self.sql_text_source.tag_add(tag, start, end)
            self.sql_text_target.tag_add(tag, start, end)

        self.set_sql_text_state('disabled')

    def get_tag(self, result: KeyColumnComparisonResult):
        type_match = result.type_name_match and result.precision_match and result.sacle_match
        if result.key.match and result.key.order_match and type_match:
            return self.TAG_DIFF_MATCH
        elif result.key.match and not result.key.order_match and type_match:
            return self.TAG_DIFF_ORDER_DONT_MATCH
        elif result.key.match and result.key.order_match and not type_match:
            return self.TAG_DIFF_TYPE_DONT_MATCH
        elif result.key.match and not result.key.order_match and not type_match:
            print('nomatch order')
            return self.TAG_DIFF_NO_MATCH_AND_ORDER
        elif not result.key.match:
            print('dontexists')
            return self.TAG_DIFF_TYPE_DONT_EXIST
        return ''

    def sql_text_clear(self):
        for i in (self.sql_text_source, self.sql_text_target):
            i.delete('1.0', tk.END)

    def set_sql_text_state(self, state):
        for i in (self.sql_text_source, self.sql_text_target):
            # i.put_styled_text()
            i.configure(state=state)

    def on_yscrollcommand_source(self, first, last):
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
        if not self.has_text_scrollbars_the_same_position():
            view_pos = self.sql_text_target.xview()
            self.sql_text_source.xview_moveto(view_pos[0])

    def has_text_scrollbars_the_same_position(self):
        return self.sql_text_source.hbar.get() == self.sql_text_target.hbar.get() and \
               self.sql_text_source.vbar.get() == self.sql_text_target.vbar.get()
