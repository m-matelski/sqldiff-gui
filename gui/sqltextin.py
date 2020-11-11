import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
# from tkinter.scrolledtext import ScrolledText

import sqlparse

from gui.custom_widgets import ModifiedTextMixin





# Based on original tk.ScrolledText source code
class ScrolledText(tk.Text):
    def __init__(self, master=None, **kw):
        self.frame = tk.Frame(master)

        self.vbar = tk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.hbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})


        tk.Text.__init__(self, self.frame, **kw)

        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)




class ScrolledText2(tk.Text):
    def __init__(self, master=None, **kw):
        self.frame = tk.Frame(master)

        self.vbar = tk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.hbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)

        kw.update({'yscrollcommand': self._yscrollcommand})
        kw.update({'xscrollcommand': self._xscrollcommand})


        tk.Text.__init__(self, self.frame, **kw)

        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

        self.on_yscrollcommand = lambda x, y: None
        self.on_xscrollcommand = lambda x, y: None


    def _yscrollcommand(self, first, last):
        self.vbar.set(first, last)
        self.on_yscrollcommand(first, last)

    def _xscrollcommand(self, first, last):
        self.hbar.set(first, last)
        self.on_xscrollcommand(first, last)

    # def on_yscrollcommand(self, first, last):
    #     print(f'on_yscrollcommand ({first}, {last})')
    #
    # def on_xscrollcommand(self, first, last):
    #     print(f'on_xscrollcommand ({first}, {last})')




    def __str__(self):
        return str(self.frame)




# former tk.Text
class SqlText(ScrolledText2, ModifiedTextMixin):
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

        # Styles and highlighting
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



    def bind_events(self):
        self.bind('<Control-a>', self.select_all)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-y>', self.redo)
        self.bind('<Control-z>', self.undo)

    def select_all(self, event=None):
        self.tag_add("sel", 1.0, tk.END)
        return "break"

    def cut(self, event=None):
        self.event_generate("<<Cut>>")

    def copy(self, event=None):
        self.event_generate("<<Copy>>")

    def paste(self, event=None):
        self.event_generate("<<Paste>>")

    def undo(self, event=None):
        self.event_generate("<<Undo>>")
        return "break"

    def redo(self, event=None):
        self.event_generate("<<Redo>>")
        return "break"


    def get_text(self):
        """
        :return: Text Widged text without last new line character
        """
        return self.get("1.0", tk.END)[0:-1]

    def on_ui_modify(self):
        self.put_styled_text()
        pass

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



# class ScrolledSqlText(tk.Frame):
#     def __iter__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # ensure a consistent GUI size
#         # self.grid_propagate(False)
#         # implement stretchability
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#
#         # create a Text widget
#         self.txt = SqlText(self)
#         self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
#         self.txt.insert('end', 'asdasdas')
#
#         # create a Scrollbar and associate it with txt
#         # scrollb = ttk.Scrollbar(self, command=self.txt.yview)
#         # scrollb.grid(row=0, column=1, sticky='nsew')
#         # self.txt['yscrollcommand'] = scrollb.set