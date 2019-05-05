from tkinter import Tk, Label, Button, Entry, mainloop, StringVar, messagebox

class FormApp():
    def __init__(self, *args, **kwargs):
        self.root = Tk()
        self.isalive = True
        self.currentrow = 0

        pad = 10

        if 'fields' in kwargs:
            self.formfields = kwargs['fields']
        else:
            raise(Exception('No fields given.'))

        if 'title' in kwargs:
            self.title = kwargs['title']
        else:
            self.title = 'Form App'

        if 'defaults' in kwargs:
            self.defaults = kwargs['defaults']
        else:
            self.defaults = ['' for f in self.formfields]

        self.root.title(self.title)

        self.titlelabel = Label(self.root, text=self.title, padx=pad, pady=pad)
        self.titlelabel.grid(row=self.currentrow, column=0, columnspan=3)
        self.currentrow += 1

        self.formvals = [StringVar(self.root, value=d) for d in self.defaults]
        for (i, field) in enumerate(self.formfields):
            l = Label(self.root, text=(field+':'))
            l.grid(row=self.currentrow, column=0)
            e = Entry(self.root, textvariable=self.formvals[i])
            e.grid(row=self.currentrow, column=1, sticky='NSEW')
            self.currentrow += 1

        self.cancelbutton = Button(self.root, text='Cancel', command=self.cancelfcn)
        self.cancelbutton.grid(row=self.currentrow, column=0, sticky='EW')

        self.submitbutton = Button(self.root, text='Submit', command=self.submitfcn)
        self.submitbutton.grid(row=self.currentrow, column=2, sticky='EW')

        # self.root.grid_columnconfigure(0, weight=1)
        # self.root.grid_columnconfigure(2, weight=1)

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        # center in screen before showing window
        self.root.withdraw()
        self.root.update()
        self.center_window()

        self.root.deiconify()

        self.root.mainloop()

    def center_window(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        x = ws/2 - w/2
        y = hs/3 - h/2

        self.root.minsize(w, h)
        self.root.geometry('+%d+%d' % (x, y))

        self.root.grid_columnconfigure(1, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(self.root.grid_size()[1]-1, weight=1)

        # print('Window centered.')

    def getvalues(self):
        valuedict = {}
        for i in range(len(self.formfields)):
            valuedict[self.formfields[i]] = self.formvals[i].get()
        return valuedict

    def cancelfcn(self):
        self.values = {}
        self.root.destroy()

    def submitfcn(self):
        self.values = self.getvalues()
        self.root.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.values = {}
            self.root.destroy()


def getuserformvalues(fields, **kwargs):
    app = FormApp(fields=fields, **kwargs)
    return app.values

if __name__ == '__main__':

    fields = ['Name', 'Recipient', 'Value', 'Message']
    defs = ['Jonah', 'My friend', '100', 'Hello!']

    vals = getuserformvalues(fields, title='Test App', defaults=defs)
    if len(vals.keys()) > 0:
        print(vals)




