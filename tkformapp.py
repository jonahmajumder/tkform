from tkinter import *
from tkinter import messagebox # for some reason this is not included

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

        self.root.title(self.title)

        self.titlelabel = Label(self.root, text=self.title,
            padx=pad, pady=pad, font="-weight bold")
        self.titlelabel.grid(row=self.currentrow, column=0, columnspan=3)
        self.currentrow += 1

        self.formvals = []
        for (i, field) in enumerate(self.formfields):
            l = Label(self.root, text=(field.label+':'))
            l.grid(row=self.currentrow, column=0)
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
            valvar = StringVar(self.root, value='')
            return valvar
        def make_radiobutton():
            valvar = StringVar(self.root, value=field.default)
            f = Frame(self.root)
            f.grid(row=row, column=col, sticky='NSEW')
            for (i, opt) in enumerate(field.opts):
                r = Radiobutton(f, text=opt, value=opt, variable=valvar,
                    anchor=W)
                r.grid(row=0, column=i, sticky='NSEW')
                f.grid_columnconfigure(i, weight=1)
            return valvar
        def make_listbox():
            valvar = StringVar(self.root, value='')
            return valvar

        fcn_dict = {
            'entry': make_entry,
            'radiobutton': make_radiobutton,
            'checkbutton': make_checkbutton,
            'listbox': make_listbox
        }

        valvar = fcn_dict[field.widgettype]()
        return valvar


    def configure_window(self):
        # center window in screen
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        x = ws/2 - w/2
        y = hs/3 - h/2
        self.root.geometry('+%d+%d' % (x, y))

        # do not allow window to be made any smaller
        self.root.minsize(w, h)

        # set window resizing behavior
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(self.root.grid_size()[1]-1, weight=1)

        # print('Window centered.')

    def getvalues(self):
        valuedict = {}
        for i in range(len(self.formvals)):
            valuedict[self.formfields[i].label] = self.formvals[i].get()
        return valuedict

    def cancelfcn(self):
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

        strtype = type('')
        if type(args[0]) == strtype:
            self.label = args[0]
        else:
            raise(Exception('First argument (label) must be string.'))

        widgets = ['entry', 'radiobutton', 'checkbutton', 'listbox']
        if args[1].lower() in widgets:
            self.widgettype = args[1]
        else:
            raise(Exception('Invalid widget type.'))

        self.default = args[2]

        if self.widgettype in ['radiobutton', 'listbox']:
            if len(args) > 3:
                if len(args[3]) > 1:
                    if self.default in args[3]:
                        self.opts = args[3]
                    else:
                        raise(Exception('Default value must be an option.'))
                else:
                    raise(Exception('List of options must contain more than one item.'))
            else:
                raise(Exception(self.widgettype.capitalize() +
                    ' requires fourth argument for list of options.'))

if __name__ == '__main__':

    # example list of field objects
    fields = [
        FormField('Name', 'entry', 'Jonah'),
        FormField('Recipient', 'entry', 'My Friend'),
        FormField('Total cost', 'entry', '$100'),
        FormField('Message', 'entry', 'Hi!'),
        FormField('Action', 'radiobutton', 'Send', ['Send', 'Display', 'Nothing'])
    ]

    app = FormApp(fields, title='Test App')
    vals = app.values
    print(vals)




