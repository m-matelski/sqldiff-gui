import os
from tkinter import ttk

import tkinter as tk

from appdata.connections import read_connection_data, save_connection_data, connection_drivers


def set_text(entry, text):
    entry.delete(0, 'end')
    entry.insert(0, text)



class ConnectionManagerWindow(tk.Toplevel):

    DRIVERS = tuple(connection_drivers.keys())

    def __init__(self, *args, **kwargs):
        # Window
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=10)

        self.title('Connection Manager')

        # Connection list frame
        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.grid(column=0, row=0, sticky='nwes')
        self.listbox_frame.grid_rowconfigure(0, weight=1)
        self.listbox_frame.grid_columnconfigure(0, weight=1)

        # Connection listbox
        self.con_choices = []
        self.con_choicesvar = tk.StringVar(value=self.con_choices)
        self.con_listbox = tk.Listbox(self.listbox_frame, listvariable=self.con_choicesvar, selectmode='browse')
        self.con_listbox.grid(column=0, row=0, sticky='nwes', padx=5, pady=5)
        self.con_listbox.bind('<<ListboxSelect>>', self.on_connection_listbox_select)
        self.con_listbox.configure(exportselection=False)

        # Connection list buttons
        self.listbox_buttons_frame = tk.Frame(self)
        self.listbox_buttons_frame.grid(column=0, row=1, sticky='nwes')
        self.listbox_buttons_frame.grid_rowconfigure(0, weight=1)
        self.listbox_buttons_frame.grid_columnconfigure(0, weight=1)
        self.listbox_buttons_frame.grid_columnconfigure(1, weight=1)

        self.btn_add_con = ttk.Button(self.listbox_buttons_frame, text='Add', command=self.add_connection)
        self.btn_add_con.grid(column=0, row=0, sticky='ew', padx=1, pady=1)

        self.btn_delete_con = ttk.Button(self.listbox_buttons_frame, text='Delete', command=self.delete_connection)
        self.btn_delete_con.grid(column=1, row=0, sticky='ew', padx=1, pady=1)

        # Connection details
        self.details_frame = tk.Frame(self)
        self.details_frame.grid(column=1, row=0, sticky='nwes')
        self.details_frame.grid_columnconfigure(1, weight=1)

        # Form Labels
        lbl_padx = 3
        lbl_pady = 4
        self.lbl_name = ttk.Label(self.details_frame, text='Connection Name:').grid(column=0, row=0, sticky='e', padx=lbl_padx, pady=lbl_pady)
        self.lbl_host = ttk.Label(self.details_frame, text='Host:').grid(column=0, row=1, sticky='e', padx=lbl_padx, pady=lbl_pady)
        self.lbl_port = ttk.Label(self.details_frame, text='Port:').grid(column=0, row=2, sticky='e', padx=lbl_padx, pady=lbl_pady)
        self.lbl_user = ttk.Label(self.details_frame, text='User:').grid(column=0, row=3, sticky='e', padx=lbl_padx, pady=lbl_pady)
        self.lbl_pass = ttk.Label(self.details_frame, text='Password:').grid(column=0, row=4, sticky='e', padx=lbl_padx, pady=lbl_pady)
        self.lbl_db = ttk.Label(self.details_frame, text='Db:').grid(column=0, row=5, sticky='e', padx=lbl_padx, pady=lbl_pady)

        # Form Entires
        self.sv_entry = tk.StringVar()
        self.sv_host = tk.StringVar()
        self.sv_port = tk.StringVar()
        self.sv_user = tk.StringVar()
        self.sv_pass = tk.StringVar()

        ent_padx = 10
        self.ent_name = ttk.Entry(self.details_frame, textvariable=self.sv_entry)
        self.ent_name.grid(column=1, row=0, sticky='ew',padx=ent_padx)
        self.ent_name.bind('<FocusOut>', self.on_name_focus_out)

        self.ent_host = ttk.Entry(self.details_frame, textvariable=self.sv_host)
        self.ent_host.grid(column=1, row=1, sticky='ew', padx=ent_padx)
        self.ent_port = ttk.Entry(self.details_frame, textvariable=self.sv_port)
        self.ent_port.grid(column=1, row=2, sticky='ew', padx=ent_padx)
        self.ent_user = ttk.Entry(self.details_frame, textvariable=self.sv_user)
        self.ent_user.grid(column=1, row=3, sticky='ew', padx=ent_padx)
        self.ent_pass = ttk.Entry(self.details_frame, textvariable=self.sv_pass, show='*')
        self.ent_pass.grid(column=1, row=4, sticky='ew', padx=ent_padx)

        self.combo_db = ttk.Combobox(self.details_frame)
        self.combo_db['values'] = self.DRIVERS
        self.combo_db.state(['readonly'])
        self.combo_db.bind('<<ComboboxSelected>>', self.combo_db_clear_selection)
        self.combo_db.grid(column=1, row=5, sticky='ew', padx=ent_padx)

        # Window OK Cancel Buttons
        self.win_buttons_frame = tk.Frame(self)
        self.win_buttons_frame.grid(column=1, row=1, sticky='e')
        self.win_buttons_frame.grid_rowconfigure(0, weight=1)
        self.btn_ok = ttk.Button(self.win_buttons_frame, text='Ok', command=self.submit_connections)
        self.btn_ok.grid(column=1, row=0, sticky='e', padx=2)
        self.btn_cancel = ttk.Button(self.win_buttons_frame, text='Cancel', command=self.cancel_connections)
        self.btn_cancel.grid(column=0, row=0, sticky='e', padx=5)

        self.form_inputs = (
            self.ent_name,
            self.ent_host,
            self.ent_port,
            self.ent_user,
            self.ent_pass,
            self.combo_db
        )

        self.read_connection_data()
        self.selected = ''
        self.disable_form()


    def read_connection_data(self):
        self.connection_data =  read_connection_data()
        self.con_choices = list(self.connection_data.keys())
        self.con_choicesvar.set(self.con_choices)


    def save_connection_data(self):
        save_connection_data(self.connection_data)


    def add_connection(self):
        new_connection_name = 'NewConnection'
        connection_name = new_connection_name
        con_name_idx = 0
        while connection_name in self.con_choices:
            con_name_idx += 1
            connection_name = new_connection_name + str(con_name_idx)

        self.con_choices.append(connection_name)
        self.con_choicesvar.set(self.con_choices)

        self.connection_data[connection_name] = {'name': connection_name}

    def delete_connection(self):
        selected = self.con_listbox.get(self.con_listbox.curselection())

        if selected in self.con_choices:
            self.con_choices.remove(selected)
            self.con_choicesvar.set(self.con_choices)
            del self.connection_data[selected]

        self.clear_form()
        self.disable_form()

    def on_connection_listbox_select(self, event):
        curselection = self.con_listbox.curselection()
        if not curselection:
            return

        prev = self.ent_name.get()

        self.enable_form()
        if prev != self.selected and not prev == '':
            self.rename_connection(self.selected, prev)

        self.read_form()

        self.selected = self.con_listbox.get(curselection)
        print(f'selected entry {prev=}, {self.selected=}')
        self.populate_form(self.connection_data[self.selected])

    def rename_connection(self, old, new):
        if new in self.connection_data:
            raise ValueError('Cannot rename connection to existing name')

        self.connection_data[new] = self.connection_data[old]
        self.connection_data[new]['name'] = new
        del self.connection_data[old]
        # rename connection in list
        idx = self.con_choices.index(old)
        self.con_choices[idx] = new
        self.con_choicesvar.set(self.con_choices)


    def on_connection_listbox_double(self, event):
        pass

    def combo_db_clear_selection(self, event=None):
        self.combo_db.selection_clear()

    def submit_connections(self):
        self.read_form()
        self.save_connection_data()
        self.destroy()

    def cancel_connections(self):
        self.destroy()

    def on_name_focus_out(self, event):
        print('focusout name')

    def disable_form(self):
        for f in self.form_inputs:
            f.config(state='disable')

    def enable_form(self):
        for f in self.form_inputs:
            f.config(state='enable')
        self.combo_db.config(state='readonly')

    def populate_form(self, connection_entry):
        set_text(self.ent_name, connection_entry['name'])
        set_text(self.ent_host, connection_entry.get('host', ''))
        set_text(self.ent_port, connection_entry.get('port', ''))
        set_text(self.ent_user, connection_entry.get('user', ''))
        set_text(self.ent_pass, connection_entry.get('pass', ''))
        self.combo_db.set(connection_entry.get('db', ''))

    def read_form(self):
        con_name = self.ent_name.get()
        if con_name:
            connection_entry = self.connection_data[con_name]
            connection_entry['name'] = con_name
            connection_entry['host'] = self.ent_host.get()
            connection_entry['port'] = self.ent_port.get()
            connection_entry['user'] = self.ent_user.get()
            connection_entry['pass'] = self.ent_pass.get()
            connection_entry['db'] = self.combo_db.get()

    def clear_form(self):
        for f in self.form_inputs:
            set_text(f, '')







if __name__ == '__main__':
    mw = ConnectionManagerWindow()
    mw.mainloop()
