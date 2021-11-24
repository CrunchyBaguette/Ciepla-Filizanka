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
userType = "client"
userId = ""
userData = {}


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.geometry("942x705+536+145")
        self.minsize(120, 1)
        self.maxsize(2564, 2141)
        self.resizable(0, 0)
        self.title("Ciepła Filiżanka")
        self.configure(background="#d9d9d9")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame(LoginPage)

        # for F in (LoginPage, MainPage, RegisterPage, CatalogPage, TestPage, AccountPage):
        #    page_name = F.__name__
        #    frame = F(parent=self.container, controller=self)
        #    self.frames[page_name] = frame
        #
        #    # put all of the pages in the same location;
        #    # the one on the top of the stacking order
        #    # will be the one that is visible.
        #    frame.grid(row=0, column=0, sticky="nsew")

    # def show_frame(self, page_name):
    #    '''Show a frame for the given page name'''
    #    frame = self.frames[page_name]
    #    frame.tkraise()

    def show_frame(self, page):
        frame = page(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self)
        title.place(x=0, y=0, height=81, width=944)
        title.configure(font="-family {Segoe UI Black} -size 20 -weight bold -underline 1")
        title.configure(text='''Ciepła Filiżanka''')

        emailLabel = tk.Label(self)
        emailLabel.place(x=320, y=110, height=21, width=304)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text='''E-mail:''')

        emailEntry = tk.Entry(self)
        emailEntry.place(x=320, y=140, height=20, width=304)

        passwordLabel = tk.Label(self)
        passwordLabel.place(x=320, y=170, height=21, width=304)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text='''Hasło:''')

        passwordEntry = tk.Entry(self, show="*")
        passwordEntry.place(x=320, y=200, height=20, width=304)

        loginButton = tk.Button(self, command=lambda: self.login(controller, messageLabel, emailEntry, passwordEntry))
        loginButton.place(x=380, y=300, height=54, width=187)
        loginButton.configure(activebackground="#ececec")
        loginButton.configure(activeforeground="#000000")
        loginButton.configure(background="#d9d9d9")
        loginButton.configure(disabledforeground="#a3a3a3")
        loginButton.configure(foreground="#000000")
        loginButton.configure(highlightbackground="#d9d9d9")
        loginButton.configure(highlightcolor="black")
        loginButton.configure(pady="0")
        loginButton.configure(text='''Zaloguj''')

        messageLabel = tk.Label(self)
        messageLabel.place(x=320, y=250, height=21, width=304)

        signInButton = tk.Button(self, command=lambda: controller.show_frame(RegisterPage))
        signInButton.place(x=380, y=380, height=54, width=187)
        signInButton.configure(activebackground="#ececec")
        signInButton.configure(activeforeground="#000000")
        signInButton.configure(background="#d9d9d9")
        signInButton.configure(disabledforeground="#a3a3a3")
        signInButton.configure(foreground="#000000")
        signInButton.configure(highlightbackground="#d9d9d9")
        signInButton.configure(highlightcolor="black")
        signInButton.configure(pady="0")
        signInButton.configure(text='''Utwórz nowe konto''')

    def login(self, cont, label, email, password):
        global userType
        global userId
        global userData
        found = False
        emailsDB = db["users"].find({}, {"_id": 0, "email": 1})
        passwordsDB = db["users"].find({}, {"_id": 0, "password": 1})
        emails = []
        passwords = []

        for e in emailsDB:
            emails.append(e)
        for p in passwordsDB:
            passwords.append(p)

        for i in range(len(emails)):
            if email.get() == emails[i]["email"] and password.get() == passwords[i]["password"]:
                found = True
                userData = db["users"].find_one({"email": emails[i]["email"], "password": passwords[i]["password"]})
                userType = userData["type"]
                userId = userData["_id"]
                label.configure(text="")
                email.delete(0, tk.END)
                password.delete(0, tk.END)
                cont.show_frame(MainPage)
        if not found:
            label.configure(text="Wrong password or email")


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        accountButton = tk.Button(self, command=lambda: controller.show_frame(AccountPage))
        accountButton.place(x=320, y=110, height=74, width=297)
        accountButton.configure(activebackground="#ececec")
        accountButton.configure(activeforeground="#000000")
        accountButton.configure(background="#d9d9d9")
        accountButton.configure(disabledforeground="#a3a3a3")
        accountButton.configure(foreground="#000000")
        accountButton.configure(highlightbackground="#d9d9d9")
        accountButton.configure(highlightcolor="black")
        accountButton.configure(pady="0")
        accountButton.configure(text='''Konto''')

        cartButton = tk.Button(self)
        cartButton.place(x=320, y=210, height=74, width=297)
        cartButton.configure(activebackground="#ececec")
        cartButton.configure(activeforeground="#000000")
        cartButton.configure(background="#d9d9d9")
        cartButton.configure(disabledforeground="#a3a3a3")
        cartButton.configure(foreground="#000000")
        cartButton.configure(highlightbackground="#d9d9d9")
        cartButton.configure(highlightcolor="black")
        cartButton.configure(pady="0")
        cartButton.configure(text='''Koszyk''')

        favouriteButton = tk.Button(self)
        favouriteButton.place(x=320, y=310, height=74, width=297)
        favouriteButton.configure(activebackground="#ececec")
        favouriteButton.configure(activeforeground="#000000")
        favouriteButton.configure(background="#d9d9d9")
        favouriteButton.configure(disabledforeground="#a3a3a3")
        favouriteButton.configure(foreground="#000000")
        favouriteButton.configure(highlightbackground="#d9d9d9")
        favouriteButton.configure(highlightcolor="black")
        favouriteButton.configure(pady="0")
        favouriteButton.configure(text='''Ulubione''')

        catalogButton = tk.Button(self, command=lambda: controller.show_frame(CatalogPage))
        catalogButton.place(x=320, y=410, height=74, width=297)
        catalogButton.configure(activebackground="#ececec")
        catalogButton.configure(activeforeground="#000000")
        catalogButton.configure(background="#d9d9d9")
        catalogButton.configure(disabledforeground="#a3a3a3")
        catalogButton.configure(foreground="#000000")
        catalogButton.configure(highlightbackground="#d9d9d9")
        catalogButton.configure(highlightcolor="black")
        catalogButton.configure(pady="0")
        catalogButton.configure(text='''Katalog''')

        logOutButton = tk.Button(self, command=lambda: controller.show_frame(LoginPage))
        logOutButton.place(x=320, y=510, height=74, width=297)
        logOutButton.configure(activebackground="#ececec")
        logOutButton.configure(activeforeground="#000000")
        logOutButton.configure(background="#d9d9d9")
        logOutButton.configure(disabledforeground="#a3a3a3")
        logOutButton.configure(foreground="#000000")
        logOutButton.configure(highlightbackground="#d9d9d9")
        logOutButton.configure(highlightcolor="black")
        logOutButton.configure(pady="0")
        logOutButton.configure(text='''Wyloguj''')

    # Test popup window
    def open_popup(self):
        top = tk.Toplevel(self)
        top.geometry("750x250")
        top.title("Child")
        tk.Label(top, text="Hello World!", font='Mistral 18 bold').place(x=150, y=80)


class AccountPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global userData

        nameLabel = tk.Label(self)
        nameLabel.place(x=100, y=100, height=21, width=304)
        nameLabel.configure(anchor='w')
        nameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        nameLabel.configure(text="Imię")

        nameEntry = tk.Entry(self)
        nameEntry.place(x=100, y=130, height=20, width=304)
        nameEntry.insert(0, userData["name"])

        surnameLabel = tk.Label(self)
        surnameLabel.place(x=100, y=160, height=21, width=304)
        surnameLabel.configure(anchor='w')
        surnameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        surnameLabel.configure(text='''Nazwisko:''')

        surnameEntry = tk.Entry(self)
        surnameEntry.place(x=100, y=190, height=20, width=304)
        surnameEntry.insert(0, userData["surname"])

        emailLabel = tk.Label(self)
        emailLabel.place(x=100, y=220, height=21, width=304)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text='''E-mail:''')

        emailEntry = tk.Entry(self)
        emailEntry.place(x=100, y=250, height=20, width=304)
        emailEntry.insert(0, userData["email"])

        passwordLabel = tk.Label(self)
        passwordLabel.place(x=100, y=280, height=21, width=304)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text='''Hasło:''')

        passwordEntry = tk.Entry(self)
        passwordEntry.place(x=100, y=310, height=20, width=304)
        passwordEntry.insert(0, userData["password"])

        streetLabel = tk.Label(self)
        streetLabel.place(x=530, y=100, height=21, width=304)
        streetLabel.configure(anchor='w')
        streetLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        streetLabel.configure(text='''Ulica:''')

        streetEntry = tk.Entry(self)
        streetEntry.place(x=530, y=130, height=20, width=304)
        streetEntry.insert(0, userData["address"]["street"])

        numberLabel = tk.Label(self)
        numberLabel.place(x=530, y=160, height=21, width=304)
        numberLabel.configure(anchor='w')
        numberLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        numberLabel.configure(text='''Numer budynku:''')

        numberEntry = tk.Entry(self)
        numberEntry.place(x=530, y=190, height=20, width=304)
        numberEntry.insert(0, userData["address"]["number"])

        apartmentLabel = tk.Label(self)
        apartmentLabel.place(x=530, y=220, height=21, width=304)
        apartmentLabel.configure(anchor='w')
        apartmentLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        apartmentLabel.configure(text='''Numer mieszkania:''')

        apartmentEntry = tk.Entry(self)
        apartmentEntry.place(x=530, y=250, height=20, width=304)
        apartmentEntry.insert(0, userData["address"]["apartment"])

        cityLabel = tk.Label(self)
        cityLabel.place(x=530, y=280, height=21, width=304)
        cityLabel.configure(anchor='w')
        cityLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        cityLabel.configure(text='''Miasto:''')

        cityEntry = tk.Entry(self)
        cityEntry.place(x=530, y=310, height=20, width=304)
        cityEntry.insert(0, userData["address"]["city"])

        zipLabel = tk.Label(self)
        zipLabel.place(x=530, y=340, height=21, width=304)
        zipLabel.configure(anchor='w')
        zipLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        zipLabel.configure(text='''Kod pocztowy:''')

        zipEntry = tk.Entry(self)
        zipEntry.place(x=530, y=370, height=20, width=304)
        zipEntry.insert(0, userData["address"]["ZIP"])

        messageLabel = tk.Label(self)
        messageLabel.place(x=100, y=440, height=21, width=734)
        messageLabel.configure(text="")

        updateButton = tk.Button(self, command=lambda: self.change(entries))
        updateButton.place(x=380, y=490, height=64, width=177)
        updateButton.configure(activebackground="#ececec")
        updateButton.configure(activeforeground="#000000")
        updateButton.configure(background="#d9d9d9")
        updateButton.configure(disabledforeground="#a3a3a3")
        updateButton.configure(foreground="#000000")
        updateButton.configure(highlightbackground="#d9d9d9")
        updateButton.configure(highlightcolor="black")
        updateButton.configure(pady="0")
        updateButton.configure(text="Zastosuj zmiany")

        backButton = tk.Button(self, command=lambda: self.controller.show_frame(MainPage))
        backButton.place(x=380, y=570, height=64, width=177)
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text="Wróć")

        entries = [nameEntry, surnameEntry, passwordEntry, emailEntry, streetEntry, numberEntry, cityEntry,
                   zipEntry, apartmentEntry]

    # TODO
    def change(self, entries):
        return


class CatalogPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        itemsDict = []
        items = db["items"].find({}, {"_id": 0, "name": 1, "type": 1, "price": 1, "quantity": 1})

        for item in items:
            itemsDict.append({"name": item["name"], "type": item["type"], "price": item["price"],
                              "quantity": item["quantity"]})

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings', height=20)

        tree.column("# 1", anchor=tk.CENTER, width=235)
        tree.heading("# 1", text="Name", command=lambda: sortby(tree, "# 1", 0))
        tree.column("# 2", anchor=tk.CENTER, width=235)
        tree.heading("# 2", text="Type", command=lambda: sortby(tree, "# 2", 0))
        tree.column("# 3", anchor=tk.CENTER, width=235)
        tree.heading("# 3", text="Price", command=lambda: sortby(tree, "# 3", 0))
        tree.column("# 4", anchor=tk.CENTER, width=235)
        tree.heading("# 4", text="Quantity", command=lambda: sortby(tree, "# 4", 0))

        for i in range(len(itemsDict)):
            tree.insert('', 'end', text=str(i), values=(itemsDict[i]["name"], itemsDict[i]["type"],
                                                        itemsDict[i]["price"], itemsDict[i]["quantity"]))

        tree.pack()

        addCartButton = tk.Button(self)
        addCartButton.place(x=30, y=450, height=64, width=217)
        addCartButton.configure(activebackground="#ececec")
        addCartButton.configure(activeforeground="#000000")
        addCartButton.configure(background="#d9d9d9")
        addCartButton.configure(disabledforeground="#a3a3a3")
        addCartButton.configure(foreground="#000000")
        addCartButton.configure(highlightbackground="#d9d9d9")
        addCartButton.configure(highlightcolor="black")
        addCartButton.configure(pady="0")
        addCartButton.configure(text='''Dodaj do koszyka''')

        cartButton = tk.Button(self)
        cartButton.place(x=30, y=530, height=64, width=217)
        cartButton.configure(activebackground="#ececec")
        cartButton.configure(activeforeground="#000000")
        cartButton.configure(background="#d9d9d9")
        cartButton.configure(disabledforeground="#a3a3a3")
        cartButton.configure(foreground="#000000")
        cartButton.configure(highlightbackground="#d9d9d9")
        cartButton.configure(highlightcolor="black")
        cartButton.configure(pady="0")
        cartButton.configure(text='''Koszyk''')

        addFavouriteButton = tk.Button(self)
        addFavouriteButton.place(x=270, y=450, height=64, width=217)
        addFavouriteButton.configure(activebackground="#ececec")
        addFavouriteButton.configure(activeforeground="#000000")
        addFavouriteButton.configure(background="#d9d9d9")
        addFavouriteButton.configure(disabledforeground="#a3a3a3")
        addFavouriteButton.configure(foreground="#000000")
        addFavouriteButton.configure(highlightbackground="#d9d9d9")
        addFavouriteButton.configure(highlightcolor="black")
        addFavouriteButton.configure(pady="0")
        addFavouriteButton.configure(text='''Dodaj do ulubionych''')

        favouriteButton = tk.Button(self)
        favouriteButton.place(x=270, y=530, height=64, width=217)
        favouriteButton.configure(activebackground="#ececec")
        favouriteButton.configure(activeforeground="#000000")
        favouriteButton.configure(background="#d9d9d9")
        favouriteButton.configure(disabledforeground="#a3a3a3")
        favouriteButton.configure(foreground="#000000")
        favouriteButton.configure(highlightbackground="#d9d9d9")
        favouriteButton.configure(highlightcolor="black")
        favouriteButton.configure(pady="0")
        favouriteButton.configure(text='''Ulubione''')

        descriptionButton = tk.Button(self, command=lambda: self.OpisPopUp(tree))
        descriptionButton.place(x=510, y=450, height=64, width=217)
        descriptionButton.configure(activebackground="#ececec")
        descriptionButton.configure(activeforeground="#000000")
        descriptionButton.configure(background="#d9d9d9")
        descriptionButton.configure(disabledforeground="#a3a3a3")
        descriptionButton.configure(foreground="#000000")
        descriptionButton.configure(highlightbackground="#d9d9d9")
        descriptionButton.configure(highlightcolor="black")
        descriptionButton.configure(pady="0")
        descriptionButton.configure(text='''Opis produktu''')

        backButton = tk.Button(self, command=lambda: controller.show_frame(MainPage))
        backButton.place(x=510, y=530, height=64, width=217)
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text='''Powrót''')

    def OpisPopUp(self, tree):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]

            top = tk.Toplevel(self)
            top.geometry("721x370+651+258")
            top.resizable(0, 0)
            top.title(curItem[0])

            item = db["items"].find_one({"name": curItem[0]})

            opisLabel = tk.Label(top)
            opisLabel.place(x=30, y=30, height=181, width=664)
            opisLabel.configure(background="#d9d9d9")
            opisLabel.configure(disabledforeground="#a3a3a3")
            opisLabel.configure(foreground="#000000")
            opisLabel.configure(text=item["description"])
            opisLabel.configure(justify="left")
            opisLabel.configure(wraplength="660")

            returnButton = tk.Button(top, command=lambda: top.destroy())
            returnButton.place(x=310, y=260, height=54, width=107)
            returnButton.configure(activebackground="#ececec")
            returnButton.configure(activeforeground="#000000")
            returnButton.configure(background="#d9d9d9")
            returnButton.configure(disabledforeground="#a3a3a3")
            returnButton.configure(foreground="#000000")
            returnButton.configure(highlightbackground="#d9d9d9")
            returnButton.configure(highlightcolor="black")
            returnButton.configure(pady="0")
            returnButton.configure(text="Powrót")


class RegisterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        nameLabel = tk.Label(self)
        nameLabel.place(x=100, y=100, height=21, width=304)
        nameLabel.configure(anchor='w')
        nameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        nameLabel.configure(text='''Imię:''')

        nameEntry = tk.Entry(self)
        nameEntry.place(x=100, y=130, height=20, width=304)

        surnameLabel = tk.Label(self)
        surnameLabel.place(x=100, y=160, height=21, width=304)
        surnameLabel.configure(anchor='w')
        surnameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        surnameLabel.configure(text='''Nazwisko:''')

        surnameEntry = tk.Entry(self)
        surnameEntry.place(x=100, y=190, height=20, width=304)

        emailLabel = tk.Label(self)
        emailLabel.place(x=100, y=220, height=21, width=304)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text='''E-mail:''')

        emailEntry = tk.Entry(self)
        emailEntry.place(x=100, y=250, height=20, width=304)

        passwordLabel = tk.Label(self)
        passwordLabel.place(x=100, y=280, height=21, width=304)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text='''Hasło:''')

        passwordEntry = tk.Entry(self)
        passwordEntry.place(x=100, y=310, height=20, width=304)

        streetLabel = tk.Label(self)
        streetLabel.place(x=530, y=100, height=21, width=304)
        streetLabel.configure(anchor='w')
        streetLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        streetLabel.configure(text='''Ulica:''')

        streetEntry = tk.Entry(self)
        streetEntry.place(x=530, y=130, height=20, width=304)

        numberLabel = tk.Label(self)
        numberLabel.place(x=530, y=160, height=21, width=304)
        numberLabel.configure(anchor='w')
        numberLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        numberLabel.configure(text='''Numer budynku:''')

        numberEntry = tk.Entry(self)
        numberEntry.place(x=530, y=190, height=20, width=304)

        apartmentLabel = tk.Label(self)
        apartmentLabel.place(x=530, y=220, height=21, width=304)
        apartmentLabel.configure(anchor='w')
        apartmentLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        apartmentLabel.configure(text='''Numer mieszkania:''')

        apartmentEntry = tk.Entry(self)
        apartmentEntry.place(x=530, y=250, height=20, width=304)

        cityLabel = tk.Label(self)
        cityLabel.place(x=530, y=280, height=21, width=304)
        cityLabel.configure(anchor='w')
        cityLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        cityLabel.configure(text='''Miasto:''')

        cityEntry = tk.Entry(self)
        cityEntry.place(x=530, y=310, height=20, width=304)

        zipLabel = tk.Label(self)
        zipLabel.place(x=530, y=340, height=21, width=304)
        zipLabel.configure(anchor='w')
        zipLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        zipLabel.configure(text='''Kod pocztowy:''')

        zipEntry = tk.Entry(self)
        zipEntry.place(x=530, y=370, height=20, width=304)

        messageLabel = tk.Label(self)
        messageLabel.place(x=100, y=440, height=21, width=734)
        messageLabel.configure(text="")

        createButton = tk.Button(self, command=lambda: self.register(controller, entries, messageLabel))
        createButton.place(x=380, y=490, height=64, width=177)
        createButton.configure(activebackground="#ececec")
        createButton.configure(activeforeground="#000000")
        createButton.configure(background="#d9d9d9")
        createButton.configure(disabledforeground="#a3a3a3")
        createButton.configure(foreground="#000000")
        createButton.configure(highlightbackground="#d9d9d9")
        createButton.configure(highlightcolor="black")
        createButton.configure(pady="0")
        createButton.configure(text='''Stwórz konto''')

        backButton = tk.Button(self, command=lambda: self.back(controller, entries))
        backButton.place(x=380, y=570, height=64, width=177)
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text='''Wróć''')

        entries = [nameEntry, surnameEntry, passwordEntry, emailEntry, streetEntry, numberEntry, cityEntry,
                   zipEntry, apartmentEntry]

    def back(self, cont, entries):
        for e in entries:
            e.delete(0, tk.END)
        cont.show_frame(LoginPage)

    def register(self, cont, entries, messageLabel):
        users = db["users"]
        allData = True
        newUser = {}
        newUserAddress = {}
        for i in range(len(entries)):
            if entries[i].get() == "":
                if i != 8:
                    allData = False
                else:
                    messageLabel.configure(text="Please input all data")
        if allData:
            existingUser = db["users"].find_one({"email": entries[3].get()})

            if existingUser:
                messageLabel.configure(text="User with given email already exists.")
            else:
                newUser["name"] = entries[0].get()
                newUser["surname"] = entries[1].get()
                newUser["password"] = entries[2].get()
                newUser["email"] = entries[3].get()
                newUser["favourite"] = []
                newUser["type"] = "client"

                newUserAddress["street"] = entries[4].get()
                newUserAddress["number"] = entries[5].get()
                newUserAddress["city"] = entries[6].get()
                newUserAddress["ZIP"] = entries[7].get()
                newUserAddress["apartment"] = entries[8].get() if entries[8].get() != "" else ""
                newUser["address"] = newUserAddress

                users.insert_one(newUser)
                self.back(cont, entries)


# Strona do testowania funkcjonalności bazy danych
class TestPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Label1 = tk.Label(self)
        Label1.place(x=120, y=80, height=200, width=691)
        Label1.configure(background="#d9d9d9")
        Label1.configure(disabledforeground="#a3a3a3")
        Label1.configure(foreground="#000000")
        Label1.configure(text='''Label''')
        Label1.configure(justify="left")
        Label1.configure(wraplength="690")

        Button1 = tk.Button(self, command=lambda: self.test(Label1))
        Button1.place(x=400, y=400, height=44, width=137)
        Button1.configure(activebackground="#ececec")
        Button1.configure(activeforeground="#000000")
        Button1.configure(background="#d9d9d9")
        Button1.configure(disabledforeground="#a3a3a3")
        Button1.configure(foreground="#000000")
        Button1.configure(highlightbackground="#d9d9d9")
        Button1.configure(highlightcolor="black")
        Button1.configure(pady="0")
        Button1.configure(text='''Test''')

    def test(self, label):
        label.configure(text=userData["name"])


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
