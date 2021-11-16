try:
    import tkinter as tk  # python 3
    import tkinter.ttk as ttk
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import Tkinter.ttk as ttk
    import tkFont as tkfont  # python 2


def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://Admin:admin1234@cluster0.zuzxn.mongodb.net/sklep?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['sklep']


db = get_database()
user = "client"


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.geometry("600x450+718+263")
        self.minsize(120, 1)
        self.maxsize(2564, 1061)
        self.resizable(0, 0)
        self.title("Ciepła Filiżanka")
        self.configure(background="#d9d9d9")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        entry1 = tk.Entry(self)
        entry1.place(x=160, y=90, height=20, width=264)
        entry1.configure(background="white")
        entry1.configure(disabledforeground="#a3a3a3")
        entry1.configure(font="TkFixedFont")
        entry1.configure(foreground="#000000")
        entry1.configure(insertbackground="black")

        entry2 = tk.Entry(self, show="*")
        entry2.place(x=160, y=160, height=20, width=264)
        entry2.configure(background="white")
        entry2.configure(disabledforeground="#a3a3a3")
        entry2.configure(font="TkFixedFont")
        entry2.configure(foreground="#000000")
        entry2.configure(insertbackground="black")

        button1 = tk.Button(self, command=lambda: self.login(controller, label1, entry1, entry2))
        button1.place(x=270, y=230, height=24, width=41)
        button1.configure(activebackground="#ececec")
        button1.configure(activeforeground="#000000")
        button1.configure(background="#d9d9d9")
        button1.configure(disabledforeground="#a3a3a3")
        button1.configure(foreground="#000000")
        button1.configure(highlightbackground="#d9d9d9")
        button1.configure(highlightcolor="black")
        button1.configure(pady="0")
        button1.configure(text='''Login''')

        label1 = tk.Label(self)
        label1.place(x=160, y=270, height=21, width=264)
        label1.configure(background="#d9d9d9")
        label1.configure(disabledforeground="#a3a3a3")
        label1.configure(foreground="#000000")
        label1.configure(text="")

    def login(self, cont, label, login, password):
        global user
        found = False
        loginsDB = db["users"].find({}, {"_id": 0, "name": 1})
        passwordsDB = db["users"].find({}, {"_id": 0, "password": 1})
        logins = []
        passwords = []

        for l in loginsDB:
            logins.append(l)
        for p in passwordsDB:
            passwords.append(p)

        for i in range(len(logins)):
            if login.get() == logins[i]["name"] and password.get() == passwords[i]["password"]:
                found = True
                userData = db["users"].find_one({"name": logins[i]["name"], "password": passwords[i]["password"]})
                user = userData["type"]
                label.configure(text="")
                login.delete(0, tk.END)
                password.delete(0, tk.END)
                cont.show_frame("MainPage")
        if found:
            found = False
        else:
            label.configure(text="Wrong password or login")


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self)
        button1.place(x=210, y=80, height=44, width=177)
        button1.configure(activebackground="#ececec")
        button1.configure(activeforeground="#000000")
        button1.configure(background="#d9d9d9")
        button1.configure(disabledforeground="#a3a3a3")
        button1.configure(foreground="#000000")
        button1.configure(highlightbackground="#d9d9d9")
        button1.configure(highlightcolor="black")
        button1.configure(pady="0")
        button1.configure(text='''Konto''')

        button2 = tk.Button(self, command=lambda: controller.show_frame("PageTwo"))
        button2.place(x=210, y=140, height=44, width=177)
        button2.configure(activebackground="#ececec")
        button2.configure(activeforeground="#000000")
        button2.configure(background="#d9d9d9")
        button2.configure(disabledforeground="#a3a3a3")
        button2.configure(foreground="#000000")
        button2.configure(highlightbackground="#d9d9d9")
        button2.configure(highlightcolor="black")
        button2.configure(pady="0")
        button2.configure(text='''Katalog''')

        button3 = tk.Button(self, command=lambda: controller.show_frame("LoginPage"))
        button3.place(x=210, y=200, height=44, width=177)
        button3.configure(activebackground="#ececec")
        button3.configure(activeforeground="#000000")
        button3.configure(background="#d9d9d9")
        button3.configure(disabledforeground="#a3a3a3")
        button3.configure(foreground="#000000")
        button3.configure(highlightbackground="#d9d9d9")
        button3.configure(highlightcolor="black")
        button3.configure(pady="0")
        button3.configure(text='''Wyloguj''')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        itemsDict = []
        items = db["items"].find({}, {"_id": 0, "name": 1, "type": 1, "price": 1, "quantity": 1})

        for item in items:
            itemsDict.append({"name": item["name"], "type": item["type"], "price": item["price"],
                              "quantity": item["quantity"]})

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings', height=15)

        tree.column("# 1", anchor=tk.CENTER, width=150)
        tree.heading("# 1", text="Name", command=lambda: sortby(tree, "# 1", 0))
        tree.column("# 2", anchor=tk.CENTER, width=150)
        tree.heading("# 2", text="Type", command=lambda: sortby(tree, "# 2", 0))
        tree.column("# 3", anchor=tk.CENTER, width=150)
        tree.heading("# 3", text="Price", command=lambda: sortby(tree, "# 3", 0))
        tree.column("# 4", anchor=tk.CENTER, width=150)
        tree.heading("# 4", text="Quantity", command=lambda: sortby(tree, "# 4", 0))

        for i in range(len(itemsDict)):
            tree.insert('', 'end', text=str(i), values=(itemsDict[i]["name"], itemsDict[i]["type"],
                                                        itemsDict[i]["price"], itemsDict[i]["quantity"]))

        tree.pack()


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
