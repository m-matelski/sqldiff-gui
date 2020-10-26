import os
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from tkinter import N, S, E, W
from tkinter.font import Font

import sqlparse


class ModifiedTextMixin(ABC):
    """
    This class provides on_ui_modify on_modify methods to overwrite.
    Overwritining those methods allows to catch Text Widget modification
    """
    def __init__(self):
        self.is_changing = False
        self.bind('<<Modified>>', self.__handle_on_modify)

    def __handle_on_modify(self, *args, **kwargs):
        if self.edit_modified() and not self.is_changing:
            self.is_changing = True
            self.on_ui_modify()
            self.edit_modified(0)
            self.is_changing = False
        self.on_modify()

    @abstractmethod
    def on_ui_modify(self):
        """Ovewrite this class to define action for modification of Text Widged only on UI side."""
        pass

    @abstractmethod
    def on_modify(self):
        """Ovewrite this class to define action for every Text Widged modification
        (including progrmaming e.g: text.insert etc)"""
        pass




class SqlText(tk.Text, ModifiedTextMixin):
    """
    Custom Text Widget with set style for highlighting sql syntax
    """


    TAG_KEYWORD = 'keyword'
    TAG_STRING_LITERAL = 'string_literal'
    TAG_TEXT = 'text'
    TAG_NUMBER = 'number'
    TAG_COMMENT = 'comment'
    TAG_FUNCTION ='function'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ModifiedTextMixin.__init__(self)

        self.font_name = "Courier"
        self.font_size = 14

        self.font = Font(family=self.font_name, size=self.font_size)
        self.font_keyword = Font(family=self.font_name, size=self.font_size, weight='bold')
        self.font_comment = Font(family=self.font_name, size=self.font_size, weight='normal', slant='italic')
        self.configure(font=self.font)

        self.tag_configure(self.TAG_KEYWORD, font=self.font_keyword, foreground='#4433EE')
        self.tag_configure(self.TAG_STRING_LITERAL, font=self.font, foreground='#55AA33')
        self.tag_configure(self.TAG_NUMBER, font=self.font, foreground='#EE3388')
        self.tag_configure(self.TAG_COMMENT, font=self.font_comment, foreground='#AAAAAA')
        self.tag_configure(self.TAG_FUNCTION, font=self.font, foreground='#CC6633')

    def get_text(self):
        """
        :return: Text Widged text without last new line character
        """
        return self.get("1.0", tk.END)[0:-1]


    def on_ui_modify(self):
        self.put_styled_text()

    def on_modify(self):
        pass

    def _extract_sql_syntax_highlighting_recursive(self, tokens):
        """
        Recursive search of parsed query token tree
        :param tokens:
        :return: Tuples (tag, token)
        """
        for token in tokens:
            # Keywords
            if token.ttype is sqlparse.tokens.Keyword or token.ttype is sqlparse.tokens.DML:
                yield self.TAG_KEYWORD, token
            # Numbers
            elif hasattr(token.ttype, 'parent') and token.ttype.parent is sqlparse.tokens.Literal.Number:
                yield self.TAG_NUMBER, token
            # Single quotes strings
            elif token.ttype is sqlparse.tokens.Literal.String.Single:
                yield self.TAG_STRING_LITERAL, token
            # Comment
            elif hasattr(token.ttype, 'parent') and token.ttype.parent is sqlparse.tokens.Comment:
                yield self.TAG_COMMENT, token
            # Function
            elif isinstance(token, sqlparse.sql.Function):
                # return function Identifier token
                yield self.TAG_FUNCTION, token.tokens[0]
                # and analyze function params with parenthesis
                yield from self._extract_sql_syntax_highlighting_recursive(token.tokens[1])
            # No children, return token as plain text, end recursion
            elif not hasattr(token, 'tokens'):
                yield self.TAG_TEXT, token
            # Recursive search of children kens
            else:
                yield from self._extract_sql_syntax_highlighting_recursive(token.tokens)

    def extract_sql_syntax_highlighting(self, parsed_query):
        return self._extract_sql_syntax_highlighting_recursive(parsed_query.tokens)

    def _get_tagged_tokens(self, text):
        parsed = sqlparse.parse(text)
        for p in parsed:
            yield from self.extract_sql_syntax_highlighting(p)

    def get_tagged_tokens(self):
        return self._get_tagged_tokens(self.get_text())

    def put_styled_text(self):
        tagged_tokens = self.get_tagged_tokens()
        cursor_pos = self.index(tk.INSERT)
        self.delete("1.0", tk.END)
        for tag, token in tagged_tokens:
            self.insert('end', token.value, (tag,))
        self.mark_set('insert', cursor_pos)



class SqlInputPanel(tk.Frame):
    """
    Custom widget representing SqlText Widget with navigation bar.
    """
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # self.config(highlightthickness=0,
        #               highlightcolor="#37d3ff",
        #               highlightbackground="#37d3ff")

        # Top frame for inputs, located above SqlText Widget
        self.top_frame = tk.Frame(self, bd=0, relief='solid')

        # Two Frames inside top_frame alligned to left aright
        self.top_left_frame = tk.Frame(self.top_frame, bd=0, relief='solid')
        self.top_right_frame = tk.Frame(self.top_frame, bd=0, relief='solid')

        # Adding buttons to top left frame
        self.ic = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/format_text.png'))
        self.ic2 = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/database.png'))
        self.btn_1 = tk.Button(self.top_left_frame, image= self.ic)
        self.btn_2 = tk.Button(self.top_left_frame, image= self.ic2)
        self.btn_3 = tk.Button(self.top_left_frame, image= self.ic)

        # Adding buttons to top left frame
        self.ic_add_connection = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/add_connection.png'))
        self.btn_add_connection = tk.Button(self.top_right_frame, image= self.ic_add_connection)
        self.lb_connection = ttk.Combobox(self.top_right_frame, state='readonly', values=['Postgres1', 'connection2'])

        # SqlText panel inside inherited self Frame widget
        self.sql_text = SqlText(self, height=30, width=10)

        # Positioning using Grid System
        self.top_frame.grid(column=0, row=0, sticky='nwes')
        self.top_left_frame.grid(column=0, row=0, sticky='w')
        self.top_right_frame.grid(column=1, row=0, sticky='e')
        self.sql_text.grid(column=0, row=1, sticky='nwes')

        # Setting position of top left components
        self.btn_1.grid(row=0, column=0, sticky='', ipady=0, ipadx=0)
        self.btn_2.grid(row=0, column=1, sticky='')
        self.btn_3.grid(row=0, column=2, sticky='')

        # Setg position of top right bar components
        self.lb_connection.grid(column=1, row=0, sticky='')
        self.btn_add_connection.grid(column=0, row=0)

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

        # Context menu
        self.popup_menu = tk.Menu(self.sql_text, tearoff=0)
        self.popup_menu.add_command(label="Delete",command=self.donothing)
        self.popup_menu.add_command(label="Select All", command=self.donothing)
        # self.popup_menu.bind("<FocusOut>", self.popup_focus_out)

        self.bind("<Button-3>", self.popup)  # Button-2 on Aqua

    def donothing(self):
        pass

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def popup_focus_out(self):
        self.popup_menu.unpost()




class SqlCompareDualInputPanel(tk.Frame):
    """
    Custom Widget with two custom SqlPanels sside by side
    """
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Creating sql panels in main Frame
        self.sql_panel_source = SqlInputPanel(self, padx=5, pady=0)
        self.sql_panel_target = SqlInputPanel(self, padx=5, pady=0)

        # Middle frame spacing vertically Sql input panels
        self.frame_middle = tk.Frame(self)

        # Optional buttons for middle frame
        self.ic = tk.PhotoImage(file=os.path.join('gui/resources/icons/32x32/switch.png'))
        self.ic2 = tk.PhotoImage(file=os.path.join('gui/resources/icons/16x16/database.png'))
        self.btn_1 = tk.Button(self.frame_middle, image=self.ic)

        # Spacing two panels and space frame in three grid columns
        self.sql_panel_source.grid(column=0, row=0, sticky='nwes')
        self.sql_panel_target.grid(column=2, row=0, sticky='nwes')
        self.frame_middle.grid(column=1, row=0, sticky='')

        # Optional components (such as buttons) in middle frame
        # self.btn_1.grid(column=0, row= 0, sticky='') # button in

        # Setting Widgets weight
        self.grid_rowconfigure(0, weight=1) # weight not initialized so set to 1
        self.grid_columnconfigure(0, weight=10000) # Big weight differences causes that middle frame is static
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=10000)

        # self.frame_middle.grid_rowconfigure(0, weight=1)
        # self.frame_middle.grid_columnconfigure(0, weight=1)


