import tkinter as tk
from tkinter import Tk, StringVar, BooleanVar, Menu
# for some reason these are not included
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
import webbrowser
import os, sys
import math

def flatten(list_of_lists):
    flattened = []
    for item in list_of_lists:
        if type(item) is type([]):
            [flattened.append(subitem) for subitem in item]
        else:
            flattened.append(item)
    return flattened

class FormApp():
    def __init__(self, *args, **kwargs):
        self.root = Tk()
        self.isalive = True
        self.currentrow = 0

        pad = 10

        if len(args) > 0:
            self.formfields = args[0]
        else:
            raise(Exception('No fields given.'))

        if 'title' in kwargs:
            self.title = kwargs['title']
        else:
            self.title = 'Form App'

        if (sys.platform == 'darwin'):
            self.root.configure(background='#ECECEC')

        self.root.title(self.title)

        self.styler = Style()
        # print(self.styler.theme_names())
        self.styler.theme_use('aqua')

        self.styler.configure('TOptionMenu', relief='raised')

        self.styler.configure('title.TLabel', font=('TkDefaultFont', 0, 'bold'))
        print(self.styler.lookup('title.TLabel', 'background'))
        # fnt = Style().lookup('title.TLabel', 'font')
        # print(fnt)

        self.titlelabel = Label(self.root, text=self.title, style='title.TLabel')
        self.titlelabel.grid(row=self.currentrow, column=0, columnspan=3, padx=pad, pady=pad)
        self.currentrow += 1

        self.formvals = []
        for (i, field) in enumerate(self.formfields):
            l = Label(self.root, text=(field.label+':'), style='TLabel')
            l.grid(row=self.currentrow, column=0, sticky='NSW', padx=pad)
            self.formvals.append(self.make_input(field, self.currentrow, 1))
            self.currentrow += 1

        self.cancelbutton = Button(self.root, text='Cancel', command=self.cancelfcn)
        self.cancelbutton.grid(row=self.currentrow, column=0, sticky='EW')

        self.submitbutton = Button(self.root, text='Submit', command=self.submitfcn)
        self.submitbutton.grid(row=self.currentrow, column=2, sticky='EW')

        # self.root.grid_columnconfigure(0, weight=1)
        # self.root.grid_columnconfigure(2, weight=1)

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        # center in screen before showing window
        self.root.withdraw() # hide window
        self.root.update() # create window while hidden
        self.configure_window() # configure window size, etc.

        self.root.deiconify() # show window once ready

        self.root.mainloop()

    def make_input(self, field, row, col):
        def make_entry():
            valvar = StringVar(self.root, value=field.default)
            e = Entry(self.root, textvariable=valvar)
            e.grid(row=row, column=col, sticky='NSEW')
            return valvar # does the returned stringvar still carry the entry value?
        def make_checkbutton():
            valvar = BooleanVar(self.root, value=field.default)
            ch = Checkbutton(self.root, variable=valvar)
            ch.grid(row=row, column=col, sticky='NS')
            return valvar
        def make_radiobutton():
            valvar = StringVar(self.root, value=field.default)
            f = Frame(self.root)
            f.grid(row=row, column=col, sticky='NSEW')
            for (i, opt) in enumerate(field.opts):
                r = Radiobutton(f, text=opt, value=opt, variable=valvar)
                r.grid(row=0, column=i, sticky='NSEW')
                f.grid_columnconfigure(i, weight=1)
            return valvar
        def make_dropdown():
            valvar = StringVar(self.root, value=field.default)
            # cb = Combobox(self.root, textvariable=valvar, values=field.opts)
            # cb.grid(row=row, column=col, sticky='NSEW')
            def add_to_dropdown(parent, item):
                    if type(item) is type([]):
                        submenu = Menu(parent, tearoff=0)
                        for subitem in item[1:]:
                            add_to_dropdown(submenu, subitem)
                        parent.add_cascade(label=item[0], menu=submenu)
                    else:
                        # print(type(item))
                        # item here should be a string
                        parent.add_command(label=item, command=lambda: valvar.set(item))

            mb = Menubutton(self.root, textvariable=valvar)
            mb.grid(row=row, column=col, sticky='NSEW')
            mn = Menu(mb, tearoff=0)
            for opt in field.opts:
                add_to_dropdown(mn, opt)
            mb.config(menu=mn)
            return valvar
        def make_fileinput():
            def getfile(btn, stringvar, def_file):
                [fldr, rest] = os.path.split(def_file)
                [file, ext] = os.path.splitext(rest)
                ftype = ext[1:] # remove dot

                # old_width = btn.winfo_width()
                # print(old_width)
                # print(self.styler.lookup(btn.winfo_class(), 'fontsize'))
                # old_width_chars = 50#math.floor(old_width / font.nametofont(btn['font']).measure('0')) - 2
                # print(old_width_chars)
                file = filedialog.askopenfilename(initialdir=fldr, title="Select file",
                    parent=self.root, filetypes=((ftype.upper() + ' Files', '*.' + ftype), ('All Files','*.*')))
                if len(file) > 0:
                    # btn['anchor'] = E
                    stringvar.set(file)
                    # btn.configure(width=old_width_chars)
                    # print('Setting width to {}'.format(old_width))

            valvar = StringVar(self.root, value='Select a file')
            self.styler.configure('finput.TButton', anchor='left')
            b = Button(self.root, textvariable=valvar, style='finput.TButton')
            b['command'] = lambda: getfile(b, valvar, field.default)
            b.grid(row=row, column=col, sticky='NSEW')
            return valvar
        def make_link():
            def open_url(url):
                webbrowser.open_new(url)
                return 0

            valvar = StringVar(self.root, value=field.default)
            self.styler.configure('link.TLabel', foreground='blue', anchor='center')
            l = Label(self.root, text=field.default, style='link.TLabel', cursor='hand2')
            l.grid(row=row, column=col, sticky='NSEW')
            l.bind('<Button-1>', lambda e: open_url(field.default))
            return valvar # does the returned stringvar still carry the entry value?

        fcn_dict = {
            'entry': make_entry,
            'radiobutton': make_radiobutton,
            'checkbutton': make_checkbutton,
            'dropdown': make_dropdown,
            'file': make_fileinput,
            'link': make_link
        }

        valvar = fcn_dict[field.widgettype]()
        return valvar

    def configure_window(self):
        # center window in screen
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        reqw = self.root.winfo_reqwidth()
        reqh = self.root.winfo_reqheight()

        width = round(1.25 * reqw)
        height = round(reqh)

        xctr = ws/2
        yctr = hs/3

        xleft = xctr - width/2
        ytop = yctr - height/2

        self.root.geometry('+%d+%d' % (xleft, ytop))

        # do not allow window to be made any smaller
        self.root.minsize(width, height)

        # set window resizing behavior
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(self.root.grid_size()[1]-1, weight=1)

        # print('Window centered.')

    def getvalues(self):
        valuedict = {}
        for i in range(len(self.formvals)):
            if self.formfields[i].widgettype == 'file':
                if self.formvals[i].get() == 'Select a file':
                    self.formvals[i].set('')
            
            valuedict[self.formfields[i].label] = self.formvals[i].get()

        return valuedict

    def cancelfcn(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
            self.values = {}
            self.root.destroy()

    def submitfcn(self):
        self.values = self.getvalues()
        self.root.destroy()

    def on_closing(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
            self.values = {}
            self.root.destroy()

class FormField():
    def __init__(self, *args):
        flderr = Exception('Invalid field definition.')

        if len(args) < 3:
            raise(Exception('Not enough input args (expects label, widget type, default).'))

        # check if the first argument is a string (as the label, it must be)
        strtype = type('')
        if type(args[0]) == strtype:
            self.label = args[0]
        else:
            raise(Exception('First argument (label) must be string.'))

        # check that second argument specifies a supported widget type (i.e. one from this list)
        widgets = ['entry', 'radiobutton', 'checkbutton', 'dropdown', 'file', 'link']
        if args[1].lower() in widgets:
            self.widgettype = args[1]
        else:
            raise(Exception('Invalid widget type.'))


        self.default = args[2]

        # specific check for checkbutton: is the default value a boolean?
        booltype = type(True)
        boolexception = Exception('Could not parse default value to boolean.')
        if self.widgettype is 'checkbutton':
            if type(self.default) != booltype:
                try:
                    bool_attempt = eval(self.default.capitalize())
                    if type(bool_attempt) != booltype:
                        raise(boolexception)
                except Exception:
                    raise(boolexception)


        # specific checks for radio or dropdown:
        # - is there a set of options specified?
        # - is that list more than one item long?
        # - is the default one of the options?
        if self.widgettype in ['radiobutton', 'dropdown']:
            if len(args) > 3:
                if len(args[3]) > 1:
                    if self.default in flatten(args[3]):
                        self.opts = args[3]
                    else:
                        raise(Exception('Default value must be an option.'))
                else:
                    raise(Exception('List of options must contain more than one item.'))
            else:
                raise(Exception(self.widgettype.capitalize() +
                    ' requires fourth argument for list of options.'))

if __name__ == '__main__':

    simple_list = ['Option {}'.format(i) for i in range(1, 11)]
    cascaded_list = [['Group {}'.format(letter)] + ['Option {0}{1}'.format(letter,i) for i in range(1,6)] for letter in ['A', 'B', 'C']]
    # example list of field objects
    fields = [
        FormField('Name', 'entry', 'Jonah'),
        FormField('Recipient', 'file', 'C:\\Users\\jo27625\\Desktop\\Purchasing\\*.pdf'),
        FormField('Total cost', 'entry', '$100'),
        FormField('Test check', 'checkbutton', True),
        FormField('Google', 'link', 'http://www.google.com'),
        FormField('Message', 'entry', 'Hi!'),
        FormField('Action', 'radiobutton', 'Send', ['Send', 'Display', 'Nothing']),
        FormField('Dropdown', 'dropdown', 'Option 1', simple_list),
        FormField('Dropdown Cascade', 'dropdown', cascaded_list[0][1], cascaded_list)
    ]

    app = FormApp(fields, title='Test App')
    vals = app.values
    print(vals)



