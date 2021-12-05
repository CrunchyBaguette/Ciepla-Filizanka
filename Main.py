import datetime

try:
    import tkinter as tk  # python 3
    import tkinter.ttk as ttk
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import Tkinter.ttk as ttk
    import tkFont as tkfont  # python 2

from bson.objectid import ObjectId


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://Admin:admin1234@cluster0.zuzxn.mongodb.net/sklep?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['sklep']


db = get_database()
userType = "klient"
userId = ""
editedUserId = ""
userData = {}
messageString = ""


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


def disable_frame(page):
    for child in page.winfo_children():
        try:
            if child.widgetName != "frame":
                child.configure(state="disabled")
        except Exception:
            pass


def enable_frame(page):
    for child in page.winfo_children():
        try:
            if child.widgetName != "frame":
                child.configure(state="normal")
        except Exception:
            pass


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self)
        title.place(x=0, y=0, height=81, width=944)
        title.configure(font="-family {Segoe UI Black} -size 20 -weight bold -underline 1")
        title.configure(text="Ciepła Filiżanka")

        emailLabel = tk.Label(self)
        emailLabel.place(x=320, y=110, height=21, width=304)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text="E-mail:")

        emailEntry = tk.Entry(self)
        emailEntry.place(x=320, y=140, height=20, width=304)

        passwordLabel = tk.Label(self)
        passwordLabel.place(x=320, y=170, height=21, width=304)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text="Hasło:")

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
        loginButton.configure(text="Zaloguj")

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
        signInButton.configure(text="Utwórz nowe konto")

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

        accountButton = tk.Button(self, command=lambda: (setEditUser(str(userId)), controller.show_frame(AccountPage)))
        accountButton.configure(activebackground="#ececec")
        accountButton.configure(activeforeground="#000000")
        accountButton.configure(background="#d9d9d9")
        accountButton.configure(disabledforeground="#a3a3a3")
        accountButton.configure(foreground="#000000")
        accountButton.configure(highlightbackground="#d9d9d9")
        accountButton.configure(highlightcolor="black")
        accountButton.configure(pady="0")
        accountButton.configure(text="Konto")

        employeeButton = tk.Button(self, command=lambda: controller.show_frame(EmployeesPage))
        employeeButton.configure(activebackground="#ececec")
        employeeButton.configure(activeforeground="#000000")
        employeeButton.configure(background="#d9d9d9")
        employeeButton.configure(disabledforeground="#a3a3a3")
        employeeButton.configure(foreground="#000000")
        employeeButton.configure(highlightbackground="#d9d9d9")
        employeeButton.configure(highlightcolor="black")
        employeeButton.configure(pady="0")
        employeeButton.configure(text='''Pracownicy''')

        ordersButton = tk.Button(self, command=lambda: controller.show_frame(OrdersPage))
        ordersButton.configure(activebackground="#ececec")
        ordersButton.configure(activeforeground="#000000")
        ordersButton.configure(background="#d9d9d9")
        ordersButton.configure(disabledforeground="#a3a3a3")
        ordersButton.configure(foreground="#000000")
        ordersButton.configure(highlightbackground="#d9d9d9")
        ordersButton.configure(highlightcolor="black")
        ordersButton.configure(pady="0")
        ordersButton.configure(text="Historia zamówień")

        cartButton = tk.Button(self, command=lambda: controller.show_frame(CartPage))
        cartButton.configure(activebackground="#ececec")
        cartButton.configure(activeforeground="#000000")
        cartButton.configure(background="#d9d9d9")
        cartButton.configure(disabledforeground="#a3a3a3")
        cartButton.configure(foreground="#000000")
        cartButton.configure(highlightbackground="#d9d9d9")
        cartButton.configure(highlightcolor="black")
        cartButton.configure(pady="0")
        cartButton.configure(text="Koszyk")

        favouriteButton = tk.Button(self, command=lambda: controller.show_frame(FavouritePage))
        favouriteButton.configure(activebackground="#ececec")
        favouriteButton.configure(activeforeground="#000000")
        favouriteButton.configure(background="#d9d9d9")
        favouriteButton.configure(disabledforeground="#a3a3a3")
        favouriteButton.configure(foreground="#000000")
        favouriteButton.configure(highlightbackground="#d9d9d9")
        favouriteButton.configure(highlightcolor="black")
        favouriteButton.configure(pady="0")
        favouriteButton.configure(text="Ulubione")

        catalogButton = tk.Button(self, command=lambda: controller.show_frame(CatalogPage))
        catalogButton.configure(activebackground="#ececec")
        catalogButton.configure(activeforeground="#000000")
        catalogButton.configure(background="#d9d9d9")
        catalogButton.configure(disabledforeground="#a3a3a3")
        catalogButton.configure(foreground="#000000")
        catalogButton.configure(highlightbackground="#d9d9d9")
        catalogButton.configure(highlightcolor="black")
        catalogButton.configure(pady="0")
        catalogButton.configure(text="Katalog")

        logOutButton = tk.Button(self, command=lambda: controller.show_frame(LoginPage))
        logOutButton.configure(activebackground="#ececec")
        logOutButton.configure(activeforeground="#000000")
        logOutButton.configure(background="#d9d9d9")
        logOutButton.configure(disabledforeground="#a3a3a3")
        logOutButton.configure(foreground="#000000")
        logOutButton.configure(highlightbackground="#d9d9d9")
        logOutButton.configure(highlightcolor="black")
        logOutButton.configure(pady="0")
        logOutButton.configure(text="Wyloguj")

        if userType == "klient":
            accountButton.place(x=320, y=50, height=74, width=297)
            ordersButton.place(x=320, y=150, height=74, width=297)
            cartButton.place(x=320, y=250, height=74, width=297)
            favouriteButton.place(x=320, y=350, height=74, width=297)
            catalogButton.place(x=320, y=450, height=74, width=297)
            logOutButton.place(x=320, y=550, height=74, width=297)
        elif userType == "właściciel":
            accountButton.place(x=320, y=110, height=74, width=297)
            employeeButton.place(x=320, y=210, height=74, width=297)
            ordersButton.place(x=320, y=310, height=74, width=297)
            ordersButton.configure(text="Zamówienia")
            catalogButton.place(x=320, y=410, height=74, width=297)
            logOutButton.place(x=320, y=510, height=74, width=297)
        elif userType == "pracownik":
            accountButton.place(x=320, y=150, height=74, width=297)
            ordersButton.place(x=320, y=250, height=74, width=297)
            ordersButton.configure(text="Zamówienia")
            catalogButton.place(x=320, y=350, height=74, width=297)
            logOutButton.place(x=320, y=450, height=74, width=297)


class AccountPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global editedUserId
        editedUser = db["users"].find_one({"_id": ObjectId(editedUserId)})

        nameLabel = tk.Label(self)
        nameLabel.configure(anchor='w')
        nameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        nameLabel.configure(text="Imię")

        nameEntry = tk.Entry(self)
        nameEntry.insert(0, editedUser["name"])

        surnameLabel = tk.Label(self)
        surnameLabel.configure(anchor='w')
        surnameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        surnameLabel.configure(text="Nazwisko:")

        surnameEntry = tk.Entry(self)
        surnameEntry.insert(0, editedUser["surname"])

        emailLabel = tk.Label(self)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text="E-mail")

        emailEntry = tk.Entry(self)
        emailEntry.insert(0, editedUser["email"])

        passwordLabel = tk.Label(self)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text="Hasło")

        passwordEntry = tk.Entry(self)
        passwordEntry.insert(0, editedUser["password"])

        messageLabel = tk.Label(self)
        messageLabel.place(x=100, y=440, height=21, width=734)
        messageLabel.configure(text="")

        updateButton = tk.Button(self, command=lambda: self.change(entries, messageLabel, editedUser, newsletter))
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

        entries = [nameEntry, surnameEntry, passwordEntry, emailEntry]

        if editedUser["type"] == "klient":
            nameLabel.place(x=100, y=100, height=21, width=304)
            nameEntry.place(x=100, y=130, height=20, width=304)
            surnameLabel.place(x=100, y=160, height=21, width=304)
            surnameEntry.place(x=100, y=190, height=20, width=304)
            emailLabel.place(x=100, y=220, height=21, width=304)
            emailEntry.place(x=100, y=250, height=20, width=304)
            passwordLabel.place(x=100, y=280, height=21, width=304)
            passwordEntry.place(x=100, y=310, height=20, width=304)

            newsletterRadio = tk.Checkbutton(self)
            newsletterRadio.place(x=90, y=360, height=42, width=139)
            newsletterRadio.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
            newsletterRadio.configure(text="Newsletter")
            newsletter = tk.IntVar()
            if editedUser["newsletter"] == True:
                newsletter.set(1)
            else:
                newsletter.set(0)
            newsletterRadio.configure(variable=newsletter)

            streetLabel = tk.Label(self)
            streetLabel.place(x=530, y=100, height=21, width=304)
            streetLabel.configure(anchor='w')
            streetLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
            streetLabel.configure(text="Ulica")

            streetEntry = tk.Entry(self)
            streetEntry.place(x=530, y=130, height=20, width=304)
            streetEntry.insert(0, editedUser["address"]["street"])

            numberLabel = tk.Label(self)
            numberLabel.place(x=530, y=160, height=21, width=304)
            numberLabel.configure(anchor='w')
            numberLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
            numberLabel.configure(text="Numer budynku:")

            numberEntry = tk.Entry(self)
            numberEntry.place(x=530, y=190, height=20, width=304)
            numberEntry.insert(0, editedUser["address"]["number"])

            apartmentLabel = tk.Label(self)
            apartmentLabel.place(x=530, y=220, height=21, width=304)
            apartmentLabel.configure(anchor='w')
            apartmentLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
            apartmentLabel.configure(text="Numer mieszkania:")

            apartmentEntry = tk.Entry(self)
            apartmentEntry.place(x=530, y=250, height=20, width=304)
            if "apartment" in editedUser["address"].keys():
                apartmentEntry.insert(0, editedUser["address"]["apartment"])

            cityLabel = tk.Label(self)
            cityLabel.place(x=530, y=280, height=21, width=304)
            cityLabel.configure(anchor='w')
            cityLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
            cityLabel.configure(text="Miasto:")

            cityEntry = tk.Entry(self)
            cityEntry.place(x=530, y=310, height=20, width=304)
            cityEntry.insert(0, editedUser["address"]["city"])

            zipLabel = tk.Label(self)
            zipLabel.place(x=530, y=340, height=21, width=304)
            zipLabel.configure(anchor='w')
            zipLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
            zipLabel.configure(text="Kod pocztowy:")

            zipEntry = tk.Entry(self)
            zipEntry.place(x=530, y=370, height=20, width=304)
            zipEntry.insert(0, editedUser["address"]["ZIP"])

            entries = [nameEntry, surnameEntry, passwordEntry, emailEntry, streetEntry, numberEntry, cityEntry,
                       zipEntry, apartmentEntry]

        else:
            nameLabel.place(x=320, y=100, height=21, width=304)
            nameEntry.place(x=320, y=130, height=20, width=304)
            surnameLabel.place(x=320, y=160, height=21, width=304)
            surnameEntry.place(x=320, y=190, height=20, width=304)
            emailLabel.place(x=320, y=220, height=21, width=304)
            emailEntry.place(x=320, y=250, height=20, width=304)
            passwordLabel.place(x=320, y=280, height=21, width=304)
            passwordEntry.place(x=320, y=310, height=20, width=304)

    def change(self, entries, messageLabel, editedUser, newsletter=None):
        global userData
        global editedUserId
        for i in range(len(entries)):
            if entries[i].get() == "" and i != 8:
                messageLabel.configure(text="Proszę wypełnić wszystkie pola")
                return

        messageLabel.configure(text="")
        if editedUser["type"] == "klient":
            addressInfo = {"street": entries[4].get(), "number": entries[5].get(), "city": entries[6].get(),
                           "ZIP": entries[7].get()}
            if entries[8].get() != "":
                addressInfo["apartment"] = entries[8].get()

            db["users"].update_one({
                "_id": ObjectId(editedUserId)
            }, {
                "$set": {
                    "address": addressInfo,
                    "newsletter": bool(newsletter.get())
                }
            })

        db["users"].update_one({
            "_id": ObjectId(editedUserId)
        }, {
            "$set": {
                "name": entries[0].get(),
                "surname": entries[1].get(),
                "password": entries[2].get(),
                "email": entries[3].get(),
            }
        })
        if userData["_id"] == ObjectId(editedUserId):
            userData = db["users"].find_one({"_id": userId})


class AddEmployeePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        nameLabel = tk.Label(self)
        nameLabel.place(x=320, y=100, height=21, width=304)
        nameLabel.configure(anchor='w')
        nameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        nameLabel.configure(text="Imię")

        nameEntry = tk.Entry(self)
        nameEntry.place(x=320, y=130, height=20, width=304)
        nameEntry.insert(0, "")

        surnameLabel = tk.Label(self)
        surnameLabel.place(x=320, y=160, height=21, width=304)
        surnameLabel.configure(anchor='w')
        surnameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        surnameLabel.configure(text="Nazwisko:")

        surnameEntry = tk.Entry(self)
        surnameEntry.place(x=320, y=190, height=20, width=304)
        surnameEntry.insert(0, "")

        emailLabel = tk.Label(self)
        emailLabel.place(x=320, y=220, height=21, width=304)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text="E-mail")

        emailEntry = tk.Entry(self)
        emailEntry.place(x=320, y=250, height=20, width=304)
        emailEntry.insert(0, "")

        passwordLabel = tk.Label(self)
        passwordLabel.place(x=320, y=280, height=21, width=304)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text="Hasło")

        passwordEntry = tk.Entry(self)
        passwordEntry.place(x=320, y=310, height=20, width=304)
        passwordEntry.insert(0, "")

        messageLabel = tk.Label(self)
        messageLabel.place(x=100, y=440, height=21, width=734)
        messageLabel.configure(text="")

        addButton = tk.Button(self, command=lambda: self.addEmployee(entries, messageLabel))
        addButton.place(x=380, y=490, height=64, width=177)
        addButton.configure(activebackground="#ececec")
        addButton.configure(activeforeground="#000000")
        addButton.configure(background="#d9d9d9")
        addButton.configure(disabledforeground="#a3a3a3")
        addButton.configure(foreground="#000000")
        addButton.configure(highlightbackground="#d9d9d9")
        addButton.configure(highlightcolor="black")
        addButton.configure(pady="0")
        addButton.configure(text="Dodaj pracownika")

        backButton = tk.Button(self, command=lambda: self.controller.show_frame(EmployeesPage))
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

        entries = [nameEntry, surnameEntry, passwordEntry, emailEntry]

    def addEmployee(self, entries, messageLabel):
        for entry in entries:
            if entry.get() == "":
                messageLabel.configure(text="Proszę wpisać wszystkie dane")
                return

        existingUser = db["users"].find_one({"email": entries[3].get()})
        if existingUser:
            messageLabel.configure(text="Użytkownik z podanym emailem już istnieje")
            return

        db["users"].insert_one({
            "name": entries[0].get(),
            "surname": entries[1].get(),
            "password": entries[2].get(),
            "email": entries[3].get(),
            "type": "pracownik"
        })

        for entry in entries:
            entry.delete(0, tk.END)

        messageLabel.configure(text="Pomyślnie dodano pracownika")






class CartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        orderPrice = 0
        itemsDict = []
        order = db["orders"].find_one({"clientId": userId, "status": "koszyk"},
                                      {"_id": 1, "itemList": 1, "totalPrice": 1})

        for item in order["itemList"]:
            itemData = db["items"].find_one({"_id": item["itemId"]}, {"_id": 1, "name": 1, "price": 1})
            orderPrice += item["itemCount"] * itemData["price"]
            itemsDict.append({"name": itemData["name"], "price": itemData["price"], "count": item["itemCount"],
                              "total price": round(item["itemCount"] * itemData["price"], 2),
                              "itemId": itemData["_id"]})

        orderPrice = round(orderPrice, 2)
        db["orders"].update_one({
            "clientId": userId,
            "status": "koszyk"
        }, {
            "$set": {
                "totalPrice": orderPrice
            }
        })

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=20)

        tree["columns"] = ("# 1", "# 2", "# 3", "# 4", "# 5")
        tree.column("# 1", anchor=tk.CENTER, width=235)
        tree.heading("# 1", text="Name")
        tree.column("# 2", anchor=tk.CENTER, width=235)
        tree.heading("# 2", text="Price")
        tree.column("# 3", anchor=tk.CENTER, width=235)
        tree.heading("# 3", text="Count")
        tree.column("# 4", anchor=tk.CENTER, width=235)
        tree.heading("# 4", text="Total price")
        tree.column("# 5", anchor=tk.CENTER, width=235)
        tree.heading("# 5", text="Id")

        tree["displaycolumns"] = ("# 1", "# 2", "# 3", "# 4")

        for i in range(len(itemsDict)):
            tree.insert('', 'end', text=str(i), values=(itemsDict[i]["name"], itemsDict[i]["price"],
                                                        itemsDict[i]["count"], itemsDict[i]["total price"],
                                                        itemsDict[i]["itemId"]))

        tree.pack()

        changeCountButton = tk.Button(self, command=lambda: self.changeCountPopUp(tree, controller))
        changeCountButton.place(x=30, y=450, height=64, width=217)
        changeCountButton.configure(activebackground="#ececec")
        changeCountButton.configure(activeforeground="#000000")
        changeCountButton.configure(background="#d9d9d9")
        changeCountButton.configure(disabledforeground="#a3a3a3")
        changeCountButton.configure(foreground="#000000")
        changeCountButton.configure(highlightbackground="#d9d9d9")
        changeCountButton.configure(highlightcolor="black")
        changeCountButton.configure(pady="0")
        changeCountButton.configure(text="Zmień ilość produktu")

        deleteButton = tk.Button(self, command=lambda: self.deleteFromCart(tree, controller))
        deleteButton.place(x=270, y=450, height=64, width=217)
        deleteButton.configure(activebackground="#ececec")
        deleteButton.configure(activeforeground="#000000")
        deleteButton.configure(background="#d9d9d9")
        deleteButton.configure(disabledforeground="#a3a3a3")
        deleteButton.configure(foreground="#000000")
        deleteButton.configure(highlightbackground="#d9d9d9")
        deleteButton.configure(highlightcolor="black")
        deleteButton.configure(pady="0")
        deleteButton.configure(text="Usuń produkt z koszyka")

        orderButton = tk.Button(self, command=lambda: self.paymentAndDeliveryPopUp(order["_id"], controller))
        orderButton.place(x=510, y=450, height=64, width=217)
        orderButton.configure(activebackground="#ececec")
        orderButton.configure(activeforeground="#000000")
        orderButton.configure(background="#d9d9d9")
        orderButton.configure(disabledforeground="#a3a3a3")
        orderButton.configure(foreground="#000000")
        orderButton.configure(highlightbackground="#d9d9d9")
        orderButton.configure(highlightcolor="black")
        orderButton.configure(pady="0")
        orderButton.configure(text="Złóż zamówienie")

        quitButton = tk.Button(self, command=lambda: controller.show_frame(MainPage))
        quitButton.place(x=30, y=530, height=64, width=217)
        quitButton.configure(activebackground="#ececec")
        quitButton.configure(activeforeground="#000000")
        quitButton.configure(background="#d9d9d9")
        quitButton.configure(disabledforeground="#a3a3a3")
        quitButton.configure(foreground="#000000")
        quitButton.configure(highlightbackground="#d9d9d9")
        quitButton.configure(highlightcolor="black")
        quitButton.configure(pady="0")
        quitButton.configure(text="Powrót")

        totalPriceLabel = tk.Label(self)
        totalPriceLabel.place(x=30, y=630, height=41, width=884)
        totalPriceLabel.configure(font="-family {Segoe UI} -size 15")
        totalPriceLabel.configure(text="Koszt zamówienia: " + str(orderPrice))

    def changeCountPopUp(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            item = tree.item(tree.focus())["values"]

            disable_frame(self)
            top = tk.Toplevel(self)
            top.geometry("288x185+776+334")
            top.resizable(0, 0)
            top.title("Change Count")
            top.protocol("WM_DELETE_WINDOW", lambda: (enable_frame(self), top.destroy()))

            count = tk.StringVar(top)
            count.set(str(item[2]))

            messageLabel = tk.Label(top)
            messageLabel.place(x=30, y=20, height=21, width=224)
            messageLabel.configure(text="Podaj liczbę produktu w koszyku")

            spinbox = tk.Spinbox(top, from_=1.0, to=100.0)
            spinbox.place(x=70, y=50, height=19, width=145)
            spinbox.configure(activebackground="#f9f9f9")
            spinbox.configure(background="white")
            spinbox.configure(buttonbackground="#d9d9d9")
            spinbox.configure(disabledforeground="#a3a3a3")
            spinbox.configure(font="TkDefaultFont")
            spinbox.configure(foreground="black")
            spinbox.configure(highlightbackground="black")
            spinbox.configure(highlightcolor="black")
            spinbox.configure(insertbackground="black")
            spinbox.configure(selectbackground="blue")
            spinbox.configure(selectforeground="white")
            spinbox.configure(textvariable=count)

            changeButton = tk.Button(top, command=lambda: self.changeCount(top, spinbox, item, cont))
            changeButton.place(x=90, y=90, height=44, width=107)
            changeButton.configure(activebackground="#ececec")
            changeButton.configure(activeforeground="#000000")
            changeButton.configure(background="#d9d9d9")
            changeButton.configure(disabledforeground="#a3a3a3")
            changeButton.configure(foreground="#000000")
            changeButton.configure(highlightbackground="#d9d9d9")
            changeButton.configure(highlightcolor="black")
            changeButton.configure(pady="0")
            changeButton.configure(text="Zmień ilość")

    def changeCount(self, top, spinbox, item, cont):
        items = db["orders"].find_one({"clientId": userId, "status": "koszyk"}, {"_id": 0, "itemList": 1})
        try:
            newCount = int(float(spinbox.get()))
        except Exception:
            top.destroy()
            cont.show_frame(CartPage)
            return
        else:
            for i in items["itemList"]:
                if str(i["itemId"]) == item[4]:
                    itemQuantity = db["items"].find_one({"_id": ObjectId(item[4])})["quantity"]
                    if newCount > itemQuantity:
                        newCount = itemQuantity
                    elif newCount <= 0:
                        return

                    i["itemCount"] = newCount
                    break

            db["orders"].update_one({
                "clientId": userId,
                "status": "koszyk"
            }, {
                "$set": {
                    "itemList": items["itemList"]
                }
            })

            top.destroy()
            cont.show_frame(CartPage)

    def deleteFromCart(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            items = db["orders"].find_one({"clientId": userId, "status": "koszyk"},
                                          {"_id": 0, "itemList": 1})["itemList"]

            for i in range(len(items)):
                if str(items[i]["itemId"]) == curItem[4]:
                    items.pop(i)
                    db["orders"].update_one({
                        "clientId": userId,
                        "status": "koszyk"
                    }, {
                        "$set": {
                            "itemList": items
                        }
                    })
                    break

            cont.show_frame(CartPage)

    def paymentAndDeliveryPopUp(self, cartId, cont):
        cart = db["orders"].find_one({"_id": cartId})
        if not cart["itemList"]:
            return
        else:
            top = tk.Toplevel(self)
            top.geometry("369x211+634+254")
            top.minsize(120, 1)
            top.maxsize(2564, 2141)
            top.resizable(0, 0)
            top.title("Przetwarzanie zamówienia")
            top.configure(background="#d9d9d9")
            top.configure(highlightbackground="#d9d9d9")
            top.configure(highlightcolor="black")
            disable_frame(self)
            top.protocol("WM_DELETE_WINDOW", lambda: (enable_frame(self), top.destroy()))

            paymentOptions = ["BLIK", "Przelewy24"]
            deliveryOptions = ["kurier", "odbiór osobisty"]
            payment = tk.StringVar(top)
            payment.set(paymentOptions[0])
            delivery = tk.StringVar(top)
            delivery.set(deliveryOptions[0])

            paymentLabel = tk.Label(top)
            paymentLabel.place(x=100, y=20, height=21, width=164)
            paymentLabel.configure(text="Wybierz metodę płatności")

            paymentChoice = tk.OptionMenu(top, payment, *paymentOptions)
            paymentChoice.place(x=100, y=50, height=19, width=165)

            deliveryLabel = tk.Label(top)
            deliveryLabel.place(x=100, y=80, height=21, width=164)
            deliveryLabel.configure(text="Wybierz sposób dostawy")

            deliveryChoice = tk.OptionMenu(top, delivery, *deliveryOptions)
            deliveryChoice.place(x=100, y=110, height=19, width=165)

            NextButton = tk.Button(top, command=lambda: (self.enterAddressPopUp(top, cont, cartId, delivery.get(), payment.get()),
                                                         enable_frame(self), top.destroy()))
            NextButton.place(x=130, y=140, height=44, width=107)
            NextButton.configure(activebackground="#ececec")
            NextButton.configure(activeforeground="#000000")
            NextButton.configure(background="#d9d9d9")
            NextButton.configure(disabledforeground="#a3a3a3")
            NextButton.configure(foreground="#000000")
            NextButton.configure(highlightbackground="#d9d9d9")
            NextButton.configure(highlightcolor="black")
            NextButton.configure(pady="0")
            NextButton.configure(text="Dalej")

    def enterAddressPopUp(self, win, cont, cartId, deliveryChoice, paymentChoice):
        if deliveryChoice == "odbiór osobisty":
            self.placeOrder(win, cont, cartId, deliveryChoice, paymentChoice)
        else:
            top = tk.Toplevel(self)
            top.geometry("547x687+617+129")
            top.minsize(120, 1)
            top.maxsize(2564, 2141)
            top.resizable(0, 0)
            top.title("Podaj adres")
            top.configure(background="#d9d9d9")
            disable_frame(self)
            top.protocol("WM_DELETE_WINDOW", lambda: (enable_frame(self), top.destroy()))

            topLabel = tk.Label(top)
            topLabel.place(x=0, y=20, height=21, width=544)
            topLabel.configure(background="#d9d9d9")
            topLabel.configure(text="Podaj adres dostawy zamówienia:")

            streetLabel = tk.Label(top)
            streetLabel.place(x=0, y=70, height=21, width=544)
            streetLabel.configure(background="#d9d9d9")
            streetLabel.configure(text="Ulica:")

            streetEntry = tk.Entry(top)
            streetEntry.place(x=80, y=100, height=20, width=384)

            numberLabel = tk.Label(top)
            numberLabel.place(x=0, y=150, height=21, width=544)
            numberLabel.configure(background="#d9d9d9")
            numberLabel.configure(text="Numer domu:")

            numberEntry = tk.Entry(top)
            numberEntry.place(x=80, y=180, height=20, width=384)

            apartmentLabel = tk.Label(top)
            apartmentLabel.place(x=0, y=230, height=21, width=544)
            apartmentLabel.configure(background="#d9d9d9")
            apartmentLabel.configure(text="Numer mieszkania:")

            apartmentEntry = tk.Entry(top)
            apartmentEntry.place(x=80, y=260, height=20, width=384)

            cityLabel = tk.Label(top)
            cityLabel.place(x=0, y=310, height=21, width=544)
            cityLabel.configure(background="#d9d9d9")
            cityLabel.configure(text="Miasto:")

            cityEntry = tk.Entry(top)
            cityEntry.place(x=80, y=340, height=20, width=384)

            zipLabel = tk.Label(top)
            zipLabel.place(x=0, y=390, height=21, width=544)
            zipLabel.configure(background="#d9d9d9")
            zipLabel.configure(text="Kod pocztowy:")

            zipEntry = tk.Entry(top)
            zipEntry.place(x=80, y=420, height=20, width=384)

            defaultButton = tk.Button(top, command=lambda: self.inputDefaultAddress(entries))
            defaultButton.place(x=170, y=490, height=54, width=207)
            defaultButton.configure(activebackground="#ececec")
            defaultButton.configure(activeforeground="#000000")
            defaultButton.configure(background="#d9d9d9")
            defaultButton.configure(disabledforeground="#a3a3a3")
            defaultButton.configure(foreground="#000000")
            defaultButton.configure(highlightbackground="#d9d9d9")
            defaultButton.configure(highlightcolor="black")
            defaultButton.configure(pady="0")
            defaultButton.configure(text="Użyj domyślnego adresu")

            nextButton = tk.Button(top, command= lambda: self.placeOrder(top, cont, cartId, deliveryChoice,
                                                                         paymentChoice, messageLabel, entries))
            nextButton.place(x=170, y=570, height=54, width=207)
            nextButton.configure(activebackground="#ececec")
            nextButton.configure(activeforeground="#000000")
            nextButton.configure(background="#d9d9d9")
            nextButton.configure(disabledforeground="#a3a3a3")
            nextButton.configure(foreground="#000000")
            nextButton.configure(highlightbackground="#d9d9d9")
            nextButton.configure(highlightcolor="black")
            nextButton.configure(pady="0")
            nextButton.configure(text="Dalej")

            messageLabel = tk.Label(top)
            messageLabel.place(x=0, y=650, height=31, width=544)
            messageLabel.configure(background="#d9d9d9")

            entries = [streetEntry, numberEntry, apartmentEntry, cityEntry, zipEntry]

    def inputDefaultAddress(self, entries):
        entries[0].insert(0, userData["address"]["street"])
        entries[1].insert(0, userData["address"]["number"])
        if "apartment" in userData["address"].keys():
            entries[2].insert(0, userData["address"]["apartment"])
        entries[3].insert(0, userData["address"]["city"])
        entries[4].insert(0, userData["address"]["ZIP"])

    def placeOrder(self, top, cont, cartId, deliveryChoice, paymentChoice, messageLabel=None, entries=None):
        if deliveryChoice != "odbiór osobisty":
            for i in range(len(entries)):
                if entries[i] == "" and i != 2:
                    messageLabel.configure(text="Please input all necessary data")
                    return
            addressInfo = {"street": entries[0].get(), "number": entries[1].get(), "city": entries[3].get(),
                           "ZIP": entries[4].get()}
            if entries[2] != "":
                addressInfo["apartment"] = entries[2].get()
            db["orders"].update_one({"clientId": userData["_id"], "status": "koszyk"}, {
                "$set": {
                    "address": addressInfo,
                }
            })

        db["orders"].update_one({"clientId": userData["_id"], "status": "koszyk"},{
            "$set": {
                "delivery": deliveryChoice,
                "payment": paymentChoice,
                "status": "przyjęte",
                "orderDate": datetime.datetime.now().replace(microsecond=0)
            }
        })

        orderDesc = CreateOrderText(str(cartId))

        db["orders"].update_one({"_id": cartId},{
            "$set": {
                "orderDesc": orderDesc
            },
            "$unset": {
                "itemList": ""
            }
        })

        db["orders"].insert_one({
            "clientId": userData["_id"],
            "itemList": [],
            "totalPrice": 0.0,
            "status": "koszyk",
        })

        enable_frame(self)
        cont.show_frame(CartPage)
        top.destroy()


class FavouritePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global messageString

        itemsDict = []
        favouriteList = db["users"].find_one({"_id": userId})["favourite"]
        for itemId in favouriteList:
            item = db["items"].find_one({"_id": itemId})
            itemsDict.append({"name": item["name"], "type": item["type"], "price": item["price"],
                              "quantity": item["quantity"], "id": item["_id"]})

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings', height=20)

        tree["columns"] = ("# 1", "# 2", "# 3", "# 4", "# 5")
        tree.column("# 1", anchor=tk.CENTER, width=235)
        tree.heading("# 1", text="Name", command=lambda: sortby(tree, "# 1", 0))
        tree.column("# 2", anchor=tk.CENTER, width=235)
        tree.heading("# 2", text="Type", command=lambda: sortby(tree, "# 2", 0))
        tree.column("# 3", anchor=tk.CENTER, width=235)
        tree.heading("# 3", text="Price", command=lambda: sortby(tree, "# 3", 0))
        tree.column("# 4", anchor=tk.CENTER, width=235)
        tree.heading("# 4", text="Quantity", command=lambda: sortby(tree, "# 4", 0))
        tree["displaycolumns"] = ("# 1", "# 2", "# 3", "# 4")

        for i in range(len(itemsDict)):
            tree.insert('', 'end', text=str(i), values=(itemsDict[i]["name"], itemsDict[i]["type"],
                                                        itemsDict[i]["price"], itemsDict[i]["quantity"],
                                                        itemsDict[i]["id"]))

        tree.pack()

        addCartButton = tk.Button(self, command=lambda: addToCartPopUp(self, tree, controller, FavouritePage))
        addCartButton.place(x=30, y=450, height=64, width=217)
        addCartButton.configure(activebackground="#ececec")
        addCartButton.configure(activeforeground="#000000")
        addCartButton.configure(background="#d9d9d9")
        addCartButton.configure(disabledforeground="#a3a3a3")
        addCartButton.configure(foreground="#000000")
        addCartButton.configure(highlightbackground="#d9d9d9")
        addCartButton.configure(highlightcolor="black")
        addCartButton.configure(pady="0")
        addCartButton.configure(text="Dodaj do koszyka")

        cartButton = tk.Button(self, command=lambda: controller.show_frame(CartPage))
        cartButton.place(x=30, y=530, height=64, width=217)
        cartButton.configure(activebackground="#ececec")
        cartButton.configure(activeforeground="#000000")
        cartButton.configure(background="#d9d9d9")
        cartButton.configure(disabledforeground="#a3a3a3")
        cartButton.configure(foreground="#000000")
        cartButton.configure(highlightbackground="#d9d9d9")
        cartButton.configure(highlightcolor="black")
        cartButton.configure(pady="0")
        cartButton.configure(text="Koszyk")

        descriptionButton = tk.Button(self, command=lambda: OpisPopUp(self, tree))
        descriptionButton.place(x=270, y=450, height=64, width=217)
        descriptionButton.configure(activebackground="#ececec")
        descriptionButton.configure(activeforeground="#000000")
        descriptionButton.configure(background="#d9d9d9")
        descriptionButton.configure(disabledforeground="#a3a3a3")
        descriptionButton.configure(foreground="#000000")
        descriptionButton.configure(highlightbackground="#d9d9d9")
        descriptionButton.configure(highlightcolor="black")
        descriptionButton.configure(pady="0")
        descriptionButton.configure(text="Opis produktu")

        backButton = tk.Button(self, command=lambda: controller.show_frame(MainPage))
        backButton.place(x=270, y=530, height=64, width=217)
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text="Powrót")

        deleteFromFavouriteButton = tk.Button(self, command=lambda: self.deleteFromFavourite(tree, controller))
        deleteFromFavouriteButton.place(x=510, y=450, height=64, width=217)
        deleteFromFavouriteButton.configure(activebackground="#ececec")
        deleteFromFavouriteButton.configure(activeforeground="#000000")
        deleteFromFavouriteButton.configure(background="#d9d9d9")
        deleteFromFavouriteButton.configure(disabledforeground="#a3a3a3")
        deleteFromFavouriteButton.configure(foreground="#000000")
        deleteFromFavouriteButton.configure(highlightbackground="#d9d9d9")
        deleteFromFavouriteButton.configure(highlightcolor="black")
        deleteFromFavouriteButton.configure(pady="0")
        deleteFromFavouriteButton.configure(text="Usuń z ulubionych")

        messageLabel = tk.Label(self)
        messageLabel.place(x=30, y=630, height=41, width=884)
        messageLabel.configure(text=messageString)
        messageString = ""

    def deleteFromFavourite(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            favouriteItems = db["users"].find_one({"_id": userId})["favourite"]
            for i in range(len(favouriteItems)):
                if favouriteItems[i] == ObjectId(curItem[4]):
                    favouriteItems.pop(i)
                    break
            db["users"].update_one({"_id": userId}, {
                "$set": {
                    "favourite": favouriteItems
                }
            })
            cont.show_frame(FavouritePage)


class CatalogPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global messageString

        itemsDict = []
        items = db["items"].find({}, {"_id": 1, "name": 1, "type": 1, "price": 1, "quantity": 1})

        for item in items:
            itemsDict.append({"name": item["name"], "type": item["type"], "price": item["price"],
                              "quantity": item["quantity"], "id": item["_id"]})

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings', height=20)

        tree["columns"] = ("# 1", "# 2", "# 3", "# 4", "# 5")
        tree.column("# 1", anchor=tk.CENTER, width=235)
        tree.heading("# 1", text="Name", command=lambda: sortby(tree, "# 1", 0))
        tree.column("# 2", anchor=tk.CENTER, width=235)
        tree.heading("# 2", text="Type", command=lambda: sortby(tree, "# 2", 0))
        tree.column("# 3", anchor=tk.CENTER, width=235)
        tree.heading("# 3", text="Price", command=lambda: sortby(tree, "# 3", 0))
        tree.column("# 4", anchor=tk.CENTER, width=235)
        tree.heading("# 4", text="Quantity", command=lambda: sortby(tree, "# 4", 0))
        tree["displaycolumns"] = ("# 1", "# 2", "# 3", "# 4")

        for i in range(len(itemsDict)):
            tree.insert('', 'end', text=str(i), values=(itemsDict[i]["name"], itemsDict[i]["type"],
                                                        itemsDict[i]["price"], itemsDict[i]["quantity"],
                                                        itemsDict[i]["id"]))

        tree.pack()

        addCartButton = tk.Button(self, command=lambda: addToCartPopUp(self, tree, controller, CatalogPage))
        addCartButton.configure(activebackground="#ececec")
        addCartButton.configure(activeforeground="#000000")
        addCartButton.configure(background="#d9d9d9")
        addCartButton.configure(disabledforeground="#a3a3a3")
        addCartButton.configure(foreground="#000000")
        addCartButton.configure(highlightbackground="#d9d9d9")
        addCartButton.configure(highlightcolor="black")
        addCartButton.configure(pady="0")
        addCartButton.configure(text="Dodaj do koszyka")

        cartButton = tk.Button(self, command=lambda: controller.show_frame(CartPage))
        cartButton.configure(activebackground="#ececec")
        cartButton.configure(activeforeground="#000000")
        cartButton.configure(background="#d9d9d9")
        cartButton.configure(disabledforeground="#a3a3a3")
        cartButton.configure(foreground="#000000")
        cartButton.configure(highlightbackground="#d9d9d9")
        cartButton.configure(highlightcolor="black")
        cartButton.configure(pady="0")
        cartButton.configure(text="Koszyk")

        addFavouriteButton = tk.Button(self, command=lambda: self.addToFavourite(tree, messageLabel))
        addFavouriteButton.configure(activebackground="#ececec")
        addFavouriteButton.configure(activeforeground="#000000")
        addFavouriteButton.configure(background="#d9d9d9")
        addFavouriteButton.configure(disabledforeground="#a3a3a3")
        addFavouriteButton.configure(foreground="#000000")
        addFavouriteButton.configure(highlightbackground="#d9d9d9")
        addFavouriteButton.configure(highlightcolor="black")
        addFavouriteButton.configure(pady="0")
        addFavouriteButton.configure(text="Dodaj do ulubionych")

        favouriteButton = tk.Button(self, command=lambda: controller.show_frame(FavouritePage))
        favouriteButton.configure(activebackground="#ececec")
        favouriteButton.configure(activeforeground="#000000")
        favouriteButton.configure(background="#d9d9d9")
        favouriteButton.configure(disabledforeground="#a3a3a3")
        favouriteButton.configure(foreground="#000000")
        favouriteButton.configure(highlightbackground="#d9d9d9")
        favouriteButton.configure(highlightcolor="black")
        favouriteButton.configure(pady="0")
        favouriteButton.configure(text="Ulubione")

        descriptionButton = tk.Button(self, command=lambda: OpisPopUp(self, tree))
        descriptionButton.configure(activebackground="#ececec")
        descriptionButton.configure(activeforeground="#000000")
        descriptionButton.configure(background="#d9d9d9")
        descriptionButton.configure(disabledforeground="#a3a3a3")
        descriptionButton.configure(foreground="#000000")
        descriptionButton.configure(highlightbackground="#d9d9d9")
        descriptionButton.configure(highlightcolor="black")
        descriptionButton.configure(pady="0")
        descriptionButton.configure(text="Opis produktu")

        editButton = tk.Button(self, command=lambda: self.AddOrEditPopUp("edit", tree, controller))
        editButton.configure(activebackground="#ececec")
        editButton.configure(activeforeground="#000000")
        editButton.configure(background="#d9d9d9")
        editButton.configure(disabledforeground="#a3a3a3")
        editButton.configure(foreground="#000000")
        editButton.configure(highlightbackground="#d9d9d9")
        editButton.configure(highlightcolor="black")
        editButton.configure(pady="0")
        editButton.configure(text="Edytuj produkt")

        addButton = tk.Button(self, command=lambda: self.AddOrEditPopUp("add", tree, controller))
        addButton.configure(activebackground="#ececec")
        addButton.configure(activeforeground="#000000")
        addButton.configure(background="#d9d9d9")
        addButton.configure(disabledforeground="#a3a3a3")
        addButton.configure(foreground="#000000")
        addButton.configure(highlightbackground="#d9d9d9")
        addButton.configure(highlightcolor="black")
        addButton.configure(pady="0")
        addButton.configure(text="Dodaj produkt")

        deleteButton = tk.Button(self, command=lambda: self.deleteProduct(tree, controller))
        deleteButton.configure(activebackground="#ececec")
        deleteButton.configure(activeforeground="#000000")
        deleteButton.configure(background="#d9d9d9")
        deleteButton.configure(disabledforeground="#a3a3a3")
        deleteButton.configure(foreground="#000000")
        deleteButton.configure(highlightbackground="#d9d9d9")
        deleteButton.configure(highlightcolor="black")
        deleteButton.configure(pady="0")
        deleteButton.configure(text="Usuń produkt")

        backButton = tk.Button(self, command=lambda: controller.show_frame(MainPage))
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text="Powrót")

        messageLabel = tk.Label(self)
        messageLabel.place(x=30, y=630, height=41, width=884)
        messageLabel.configure(text=messageString)
        messageString = ""

        if userType == "klient":
            addCartButton.place(x=30, y=450, height=64, width=217)
            cartButton.place(x=30, y=530, height=64, width=217)
            addFavouriteButton.place(x=270, y=450, height=64, width=217)
            favouriteButton.place(x=270, y=530, height=64, width=217)
            descriptionButton.place(x=510, y=450, height=64, width=217)
            backButton.place(x=510, y=530, height=64, width=217)
        else:
            descriptionButton.place(x=30, y=450, height=64, width=217)
            backButton.place(x=30, y=530, height=64, width=217)
            if userType == "pracownik":
                addButton.place(x=270, y=450, height=64, width=217)
                editButton.place(x=270, y=530, height=64, width=217)
                deleteButton.place(x=510, y=530, height=64, width=217)

    def AddOrEditPopUp(self, option, tree, cont):
        curItem = ""
        if option == "edit":
            if tree.focus() == "":
                return
            else:
                curItem = tree.item(tree.focus())["values"]

        disable_frame(self)
        top = tk.Toplevel(self)
        top.geometry("537x744+603+124")
        top.minsize(120, 1)
        top.maxsize(2564, 2141)
        top.resizable(0, 0)
        if option == "add":
            top.title("Dodaj produkt")
        else:
            top.title("Edytuj produkt")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.protocol("WM_DELETE_WINDOW", lambda: (enable_frame(self), top.destroy()))

        nameLabel = tk.Label(top)
        nameLabel.place(x=120, y=40, height=21, width=304)
        nameLabel.configure(anchor='w')
        nameLabel.configure(background="#d9d9d9")
        nameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        nameLabel.configure(text="Nazwa produktu:")

        nameEntry = tk.Entry(top)
        nameEntry.place(x=120, y=70, height=20, width=304)

        typeLabel = tk.Label(top)
        typeLabel.place(x=120, y=100, height=21, width=304)
        typeLabel.configure(anchor='w')
        typeLabel.configure(background="#d9d9d9")
        typeLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        typeLabel.configure(text="Typ produktu:")

        typeEntry = tk.Entry(top)
        typeEntry.place(x=120, y=130, height=20, width=304)

        priceLabel = tk.Label(top)
        priceLabel.place(x=120, y=160, height=21, width=304)
        priceLabel.configure(anchor='w')
        priceLabel.configure(background="#d9d9d9")
        priceLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        priceLabel.configure(text="Koszt produktu:")

        priceEntry = tk.Entry(top)
        priceEntry.place(x=120, y=190, height=20, width=304)

        quantityLabel = tk.Label(top)
        quantityLabel.place(x=120, y=220, height=21, width=304)
        quantityLabel.configure(anchor='w')
        quantityLabel.configure(background="#d9d9d9")
        quantityLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        quantityLabel.configure(text="Ilość produktu na magazynie:")

        quantityEntry = tk.Entry(top)
        quantityEntry.place(x=120, y=250, height=20, width=304)

        descriptionLabel = tk.Label(top)
        descriptionLabel.place(x=120, y=280, height=21, width=304)
        descriptionLabel.configure(activebackground="#f9f9f9")
        descriptionLabel.configure(activeforeground="black")
        descriptionLabel.configure(anchor='w')
        descriptionLabel.configure(background="#d9d9d9")
        descriptionLabel.configure(disabledforeground="#a3a3a3")
        descriptionLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        descriptionLabel.configure(foreground="#000000")
        descriptionLabel.configure(highlightbackground="#d9d9d9")
        descriptionLabel.configure(highlightcolor="black")
        descriptionLabel.configure(text='''Opis produktu:''')

        descriptionText = tk.Text(top)
        descriptionText.place(x=40, y=310, height=174, width=454)
        descriptionText.configure(background="white")
        descriptionText.configure(font="TkTextFont")
        descriptionText.configure(foreground="black")
        descriptionText.configure(highlightbackground="#d9d9d9")
        descriptionText.configure(highlightcolor="black")
        descriptionText.configure(insertbackground="black")
        descriptionText.configure(selectbackground="blue")
        descriptionText.configure(selectforeground="white")
        descriptionText.configure(wrap="word")

        nextButton = tk.Button(top)
        nextButton.place(x=180, y=560, height=64, width=177)
        nextButton.configure(activebackground="#ececec")
        nextButton.configure(activeforeground="#000000")
        nextButton.configure(background="#d9d9d9")
        nextButton.configure(disabledforeground="#a3a3a3")
        nextButton.configure(foreground="#000000")
        nextButton.configure(highlightbackground="#d9d9d9")
        nextButton.configure(highlightcolor="black")
        nextButton.configure(pady="0")

        backButton = tk.Button(top, command=lambda: (cont.show_frame(CatalogPage), top.destroy()))
        backButton.place(x=180, y=640, height=64, width=177)
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text="Powrót")

        messageLabel = tk.Label(top)
        messageLabel.place(x=0, y=500, height=21, width=534)
        messageLabel.configure(background="#d9d9d9")
        messageLabel.configure(text="")

        entries = [nameEntry, typeEntry, priceEntry, quantityEntry, descriptionText]

        if option == "add":
            nextButton.configure(command=lambda: self.addProduct(entries, messageLabel, top, cont))
            nextButton.configure(text="Dodaj produkt")
        else:
            nextButton.configure(command=lambda: self.editProduct(curItem[4], entries, messageLabel, top, cont))
            nextButton.configure(text="Edytuj produkt")
            item = db["items"].find_one(ObjectId(curItem[4]))
            entries[0].insert(0, curItem[0])
            entries[1].insert(0, curItem[1])
            entries[2].insert(0, curItem[2])
            entries[3].insert(0, curItem[3])
            entries[4].insert(1.0, item["description"])

    def addProduct(self, entries, messageLabel, top, cont):
        global messageString
        existingProduct = db["items"].find_one({"name": entries[0].get()})
        if existingProduct:
            messageLabel.configure(text="Produkt o podanej nazwie już istnieje")
        else:
            description = entries[4].get("1.0", "end")
            description = description.replace('\n', "")
            try:
                db["items"].insert_one({
                    "name": entries[0].get(),
                    "type": entries[1].get(),
                    "description": description,
                    "price": float(entries[2].get()),
                    "quantity": int(entries[3].get())
                })
            except Exception:
                messageLabel.configure(text="Podano błędne dane")
            else:
                messageString = "Dodano produkt"
                top.destroy()
                cont.show_frame(CatalogPage)

    def editProduct(self, itemId, entries, messageLabel, top, cont):
        global messageString
        item = db["items"].find_one({"_id": ObjectId(itemId)})
        existingProduct = db["items"].find_one({"name": entries[0].get()})
        if existingProduct and existingProduct["name"] != item["name"]:
            messageLabel.configure(text="Produkt o podanej nazwie już istnieje")
        else:
            description = entries[4].get("1.0", "end")
            description = description.replace('\n', "")
            try:
                db["items"].update_one({"_id": item["_id"]},{
                    "$set": {
                        "name": entries[0].get(),
                        "type": entries[1].get(),
                        "description": description,
                        "price": float(entries[2].get()),
                        "quantity": int(entries[3].get())
                    }
                })
            except Exception:
                messageLabel.configure(text="Podano błędne dane")

            messageString = "Edycja produktu pomyślna"
            top.destroy()
            cont.show_frame(CatalogPage)


    def deleteProduct(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            updateCartsAndFavourites(curItem[4])
            db["items"].delete_one({"_id": ObjectId(curItem[4])})
            cont.show_frame(CatalogPage)


    def addToFavourite(self, tree, label):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            favourites = db["users"].find_one({"_id": userId})["favourite"]

            if ObjectId(curItem[4]) in favourites:
                label.configure(text="Produkt już znajduje się w ulubioncyh")
            else:
                favourites.append(ObjectId(curItem[4]))

                db["users"].update_one({"_id": userId}, {
                    "$set": {
                        "favourite": favourites
                    }
                })
                label.configure(text="dodano " + curItem[0] + " do ulubionych")


class OrdersPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ordersDict = []
        if userType == "klient":
            orders = db["orders"].find({"clientId": userId, "status": {"$ne": "koszyk"}})
        else:
            orders = db["orders"].find({"status": {"$ne": "koszyk"}})

        for order in orders:
            if "deliveredDate" in order.keys():
                ordersDict.append({"id": str(order["_id"]), "orderDate": order["orderDate"],
                                   "deliveryDate": order["deliveredDate"], "price": order["totalPrice"],
                                   "status": order["status"]})
            else:
                ordersDict.append({"id": str(order["_id"]), "orderDate": order["orderDate"],
                                   "deliveryDate": "", "price": order["totalPrice"],
                                   "status": order["status"]})

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=20)

        tree.column("# 1", anchor=tk.CENTER, width=188)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=tk.CENTER, width=188)
        tree.heading("# 2", text="Date of order", command=lambda: sortby(tree, "# 2", 0))
        tree.column("# 3", anchor=tk.CENTER, width=188)
        tree.heading("# 3", text="Date of delivery", command=lambda: sortby(tree, "# 3", 0))
        tree.column("# 4", anchor=tk.CENTER, width=188)
        tree.heading("# 4", text="Price")
        tree.column("# 5", anchor=tk.CENTER, width=188)
        tree.heading("# 5", text="Order status")

        for i in range(len(ordersDict)):
            tree.insert('', 'end', text=str(i), values=(ordersDict[i]["id"], ordersDict[i]["orderDate"],
                                                        ordersDict[i]["deliveryDate"], ordersDict[i]["price"],
                                                        ordersDict[i]["status"]))

        tree.pack()

        OrderDetailsButton = tk.Button(self, command=lambda: self.OrderOpisPopUp(tree))
        OrderDetailsButton.place(x=30, y=450, height=64, width=217)
        OrderDetailsButton.configure(activebackground="#ececec")
        OrderDetailsButton.configure(activeforeground="#000000")
        OrderDetailsButton.configure(background="#d9d9d9")
        OrderDetailsButton.configure(disabledforeground="#a3a3a3")
        OrderDetailsButton.configure(foreground="#000000")
        OrderDetailsButton.configure(highlightbackground="#d9d9d9")
        OrderDetailsButton.configure(highlightcolor="black")
        OrderDetailsButton.configure(pady="0")
        OrderDetailsButton.configure(text="Opis zamówienia")

        if userType == "pracownik":
            editStatusButton = tk.Button(self, command=lambda: self.SetStatusPopUp(tree, controller))
            editStatusButton.place(x=270, y=450, height=64, width=217)
            editStatusButton.configure(activebackground="#ececec")
            editStatusButton.configure(activeforeground="#000000")
            editStatusButton.configure(background="#d9d9d9")
            editStatusButton.configure(disabledforeground="#a3a3a3")
            editStatusButton.configure(foreground="#000000")
            editStatusButton.configure(highlightbackground="#d9d9d9")
            editStatusButton.configure(highlightcolor="black")
            editStatusButton.configure(pady="0")
            editStatusButton.configure(text="Zmień status")

        BackButton = tk.Button(self, command=lambda: controller.show_frame(MainPage))
        BackButton.place(x=30, y=530, height=64, width=217)
        BackButton.configure(activebackground="#ececec")
        BackButton.configure(activeforeground="#000000")
        BackButton.configure(background="#d9d9d9")
        BackButton.configure(disabledforeground="#a3a3a3")
        BackButton.configure(foreground="#000000")
        BackButton.configure(highlightbackground="#d9d9d9")
        BackButton.configure(highlightcolor="black")
        BackButton.configure(pady="0")
        BackButton.configure(text="Powrót")

    def SetStatusPopUp(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            currentStatus = curItem[4]

            top = tk.Toplevel(self)
            top.geometry("369x158+708+353")
            top.minsize(120, 1)
            top.maxsize(2564, 2141)
            top.resizable(0, 0)
            top.title("Set Status")
            top.configure(background="#d9d9d9")
            top.configure(highlightbackground="#d9d9d9")
            top.configure(highlightcolor="black")
            disable_frame(self)
            top.protocol("WM_DELETE_WINDOW", lambda: (enable_frame(self), top.destroy()))

            statusOptions = ["przyjęte", "w realizacji", "wysłane", "dostarczone"]
            for i in range(statusOptions.index(currentStatus)+1):
                statusOptions.pop(0)

            if len(statusOptions) == 0:
                top.destroy()
                return

            status = tk.StringVar(top)
            status.set(statusOptions[0])

            label = tk.Label(top)
            label.place(x=100, y=20, height=21, width=164)
            label.configure(text="Wybierz status zamówienia:")

            statusChoice = tk.OptionMenu(top, status, *statusOptions)
            statusChoice.place(x=100, y=50, height=19, width=165)

            nextButton = tk.Button(top, command=lambda: (self.setStatus(status.get(), curItem[0]), top.destroy(),
                                                         cont.show_frame(OrdersPage)))
            nextButton.place(x=130, y=90, height=44, width=107)
            nextButton.configure(activebackground="#ececec")
            nextButton.configure(activeforeground="#000000")
            nextButton.configure(background="#d9d9d9")
            nextButton.configure(disabledforeground="#a3a3a3")
            nextButton.configure(foreground="#000000")
            nextButton.configure(highlightbackground="#d9d9d9")
            nextButton.configure(highlightcolor="black")
            nextButton.configure(pady="0")
            nextButton.configure(text="Dalej")

    def setStatus(self, status, orderId):
        db["orders"].update_one({"_id": ObjectId(orderId)},{
            "$set": {
                "status": status
            }
        })

        if status == "dostarczone":
            db["orders"].update_one({"_id": ObjectId(orderId)}, {
                "$set": {
                    "deliveredDate": datetime.datetime.now().replace(microsecond=0)
                }
            })

    def OrderOpisPopUp(self, tree):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]

            top = tk.Toplevel(self)
            top.geometry("464x423+536+145")
            top.resizable(0, 0)
            top.title("Opis zamówienia " + curItem[0])

            text = db["orders"].find_one({"_id": ObjectId(curItem[0])})["orderDesc"]

            if userType != "klient":
                order = db["orders"].find_one({"_id": ObjectId(curItem[0])})
                user = db["users"].find_one({"_id": order["clientId"]})
                text += "\nINFORMACJE KLIENTA:\n"
                text += "ID KLIENTA: " + str(user["_id"]) + "\n"
                text += "IMIĘ: " + user["name"] + "\n"
                text += "NAZWISKO: " + user["surname"] + "\n"
                text += "EMAIL: " + user["email"] + "\n"

            OrderInfoText = tk.Text(top)
            OrderInfoText.place(x=0, y=0, height=424, width=464)
            OrderInfoText.configure(background="white")
            OrderInfoText.configure(font="TkTextFont")
            OrderInfoText.configure(foreground="black")
            OrderInfoText.configure(highlightbackground="#d9d9d9")
            OrderInfoText.configure(highlightcolor="black")
            OrderInfoText.configure(insertbackground="black")
            OrderInfoText.configure(selectbackground="blue")
            OrderInfoText.configure(selectforeground="white")
            OrderInfoText.configure(wrap="word")
            OrderInfoText.insert("end", text)
            OrderInfoText.configure(state=tk.DISABLED)


class EmployeesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        employeesDict = []
        emploees = db["users"].find({"type": "pracownik"})

        for employee in emploees:
            employeesDict.append({"id": str(employee["_id"]), "name": employee["name"], "surname": employee["surname"],
                                  "email": employee["email"]})

        tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4"), show='headings', height=20)

        tree.column("# 1", anchor=tk.CENTER, width=235)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=tk.CENTER, width=235)
        tree.heading("# 2", text="Name", command=lambda: sortby(tree, "# 2", 0))
        tree.column("# 3", anchor=tk.CENTER, width=235)
        tree.heading("# 3", text="Surname", command=lambda: sortby(tree, "# 3", 0))
        tree.column("# 4", anchor=tk.CENTER, width=235)
        tree.heading("# 4", text="EMAIL")

        for i in range(len(employeesDict)):
            tree.insert('', 'end', text=str(i), values=(employeesDict[i]["id"], employeesDict[i]["name"],
                                                        employeesDict[i]["surname"], employeesDict[i]["email"]))

        tree.pack()

        addEmployeeButton = tk.Button(self, command=lambda: controller.show_frame(AddEmployeePage))
        addEmployeeButton.place(x=30, y=450, height=64, width=217)
        addEmployeeButton.configure(activebackground="#ececec")
        addEmployeeButton.configure(activeforeground="#000000")
        addEmployeeButton.configure(background="#d9d9d9")
        addEmployeeButton.configure(disabledforeground="#a3a3a3")
        addEmployeeButton.configure(foreground="#000000")
        addEmployeeButton.configure(highlightbackground="#d9d9d9")
        addEmployeeButton.configure(highlightcolor="black")
        addEmployeeButton.configure(pady="0")
        addEmployeeButton.configure(text="Dodaj pracownika")

        editEmployeeButton = tk.Button(self, command=lambda: self.editEmployee(tree, controller))
        editEmployeeButton.place(x=270, y=450, height=64, width=217)
        editEmployeeButton.configure(activebackground="#ececec")
        editEmployeeButton.configure(activeforeground="#000000")
        editEmployeeButton.configure(background="#d9d9d9")
        editEmployeeButton.configure(disabledforeground="#a3a3a3")
        editEmployeeButton.configure(foreground="#000000")
        editEmployeeButton.configure(highlightbackground="#d9d9d9")
        editEmployeeButton.configure(highlightcolor="black")
        editEmployeeButton.configure(pady="0")
        editEmployeeButton.configure(text="Edytuj dane pracownika")

        deleteEmployeeButton = tk.Button(self, command=lambda: self.deleteEmployee(tree, controller))
        deleteEmployeeButton.place(x=510, y=450, height=64, width=217)
        deleteEmployeeButton.configure(activebackground="#ececec")
        deleteEmployeeButton.configure(activeforeground="#000000")
        deleteEmployeeButton.configure(background="#d9d9d9")
        deleteEmployeeButton.configure(disabledforeground="#a3a3a3")
        deleteEmployeeButton.configure(foreground="#000000")
        deleteEmployeeButton.configure(highlightbackground="#d9d9d9")
        deleteEmployeeButton.configure(highlightcolor="black")
        deleteEmployeeButton.configure(pady="0")
        deleteEmployeeButton.configure(text="Usuń pracownika")

        backButton = tk.Button(self, command=lambda: controller.show_frame(MainPage))
        backButton.place(x=30, y=530, height=64, width=217)
        backButton.configure(activebackground="#ececec")
        backButton.configure(activeforeground="#000000")
        backButton.configure(background="#d9d9d9")
        backButton.configure(disabledforeground="#a3a3a3")
        backButton.configure(foreground="#000000")
        backButton.configure(highlightbackground="#d9d9d9")
        backButton.configure(highlightcolor="black")
        backButton.configure(pady="0")
        backButton.configure(text="Powrót")

    def editEmployee(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            setEditUser(curItem[0])
            cont.show_frame(AccountPage)

    def deleteEmployee(self, tree, cont):
        if tree.focus() == "":
            return
        else:
            curItem = tree.item(tree.focus())["values"]
            db["users"].delete_one({"_id": ObjectId(curItem[0])})
            cont.show_frame(EmployeesPage)


class RegisterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        nameLabel = tk.Label(self)
        nameLabel.place(x=100, y=100, height=21, width=304)
        nameLabel.configure(anchor='w')
        nameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        nameLabel.configure(text="Imię:")

        nameEntry = tk.Entry(self)
        nameEntry.place(x=100, y=130, height=20, width=304)

        surnameLabel = tk.Label(self)
        surnameLabel.place(x=100, y=160, height=21, width=304)
        surnameLabel.configure(anchor='w')
        surnameLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        surnameLabel.configure(text="Nazwisko:")

        surnameEntry = tk.Entry(self)
        surnameEntry.place(x=100, y=190, height=20, width=304)

        emailLabel = tk.Label(self)
        emailLabel.place(x=100, y=220, height=21, width=304)
        emailLabel.configure(anchor='w')
        emailLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        emailLabel.configure(text="E-mail:")

        emailEntry = tk.Entry(self)
        emailEntry.place(x=100, y=250, height=20, width=304)

        passwordLabel = tk.Label(self)
        passwordLabel.place(x=100, y=280, height=21, width=304)
        passwordLabel.configure(anchor='w')
        passwordLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        passwordLabel.configure(text="Hasło:")

        passwordEntry = tk.Entry(self)
        passwordEntry.place(x=100, y=310, height=20, width=304)

        streetLabel = tk.Label(self)
        streetLabel.place(x=530, y=100, height=21, width=304)
        streetLabel.configure(anchor='w')
        streetLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        streetLabel.configure(text="Ulica:")

        streetEntry = tk.Entry(self)
        streetEntry.place(x=530, y=130, height=20, width=304)

        numberLabel = tk.Label(self)
        numberLabel.place(x=530, y=160, height=21, width=304)
        numberLabel.configure(anchor='w')
        numberLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        numberLabel.configure(text="Numer budynku:")

        numberEntry = tk.Entry(self)
        numberEntry.place(x=530, y=190, height=20, width=304)

        apartmentLabel = tk.Label(self)
        apartmentLabel.place(x=530, y=220, height=21, width=304)
        apartmentLabel.configure(anchor='w')
        apartmentLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        apartmentLabel.configure(text="Numer mieszkania:")

        apartmentEntry = tk.Entry(self)
        apartmentEntry.place(x=530, y=250, height=20, width=304)

        cityLabel = tk.Label(self)
        cityLabel.place(x=530, y=280, height=21, width=304)
        cityLabel.configure(anchor='w')
        cityLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        cityLabel.configure(text="Miasto:")

        cityEntry = tk.Entry(self)
        cityEntry.place(x=530, y=310, height=20, width=304)

        zipLabel = tk.Label(self)
        zipLabel.place(x=530, y=340, height=21, width=304)
        zipLabel.configure(anchor='w')
        zipLabel.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        zipLabel.configure(text="Kod pocztowy:")

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
        createButton.configure(text="Stwórz konto")

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
        backButton.configure(text="Powrót")

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
                newUser["type"] = "klient"
                newUser["newsletter"] = False

                newUserAddress["street"] = entries[4].get()
                newUserAddress["number"] = entries[5].get()
                newUserAddress["city"] = entries[6].get()
                newUserAddress["ZIP"] = entries[7].get()
                if entries[8].get() != "":
                    newUserAddress["apartment"] = entries[8].get()
                newUser["address"] = newUserAddress

                users.insert_one(newUser)
                createdUser = db["users"].find_one({"email": entries[3].get()})

                db["orders"].insert_one({
                    "clientId": createdUser["_id"],
                    "itemList": [],
                    "totalPrice": 0.0,
                    "status": "koszyk",
                })

                self.back(cont, entries)
        else:
            messageLabel.configure(text="Please input all data")


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


def addToCartPopUp(self, tree, cont, page):
    if tree.focus() == "":
        return
    elif tree.item(tree.focus())["values"][3] == 0:
        return
    else:
        item = tree.item(tree.focus())["values"]

        disable_frame(self)
        top = tk.Toplevel(self)
        top.geometry("288x185+776+334")
        top.resizable(0, 0)
        top.title("Change Count")
        top.protocol("WM_DELETE_WINDOW", lambda: (enable_frame(self), top.destroy()))

        messageLabel = tk.Label(top)
        messageLabel.place(x=30, y=20, height=21, width=224)
        messageLabel.configure(text="Podaj liczbę produktu do dodania")

        spinbox = tk.Spinbox(top, from_=1.0, to=item[3])
        spinbox.place(x=70, y=50, height=19, width=145)
        spinbox.configure(activebackground="#f9f9f9")
        spinbox.configure(background="white")
        spinbox.configure(buttonbackground="#d9d9d9")
        spinbox.configure(disabledforeground="#a3a3a3")
        spinbox.configure(font="TkDefaultFont")
        spinbox.configure(foreground="black")
        spinbox.configure(highlightbackground="black")
        spinbox.configure(highlightcolor="black")
        spinbox.configure(insertbackground="black")
        spinbox.configure(selectbackground="blue")
        spinbox.configure(selectforeground="white")

        addButton = tk.Button(top, command=lambda: addToCart(top, spinbox, item, cont, page))
        addButton.place(x=90, y=90, height=44, width=107)
        addButton.configure(activebackground="#ececec")
        addButton.configure(activeforeground="#000000")
        addButton.configure(background="#d9d9d9")
        addButton.configure(disabledforeground="#a3a3a3")
        addButton.configure(foreground="#000000")
        addButton.configure(highlightbackground="#d9d9d9")
        addButton.configure(highlightcolor="black")
        addButton.configure(pady="0")
        addButton.configure(text="Dodaj do koszyka")


def addToCart(top, spinbox, item, cont, page):
    global messageString
    alreadyInCart = False
    itemList = db["orders"].find_one({"clientId": userId, "status": "koszyk"})["itemList"]
    try:
        itemCount = int(float(spinbox.get()))
    except Exception:
        messageString = "Podano błędną ilość produktu"
        top.destroy()
        cont.show_frame(page)
    else:
        if itemCount > item[3] or itemCount <= 0:
            messageString = "Podano błędną ilość produktu"
            top.destroy()
            cont.show_frame(page)
        else:
            for product in itemList:
                if ObjectId(item[4]) in product.values():
                    alreadyInCart = True
                    break
            if alreadyInCart:
                messageString = "Produkt już znajduje się w koszyku"
                top.destroy()
                cont.show_frame(page)
            else:
                itemList.append({
                    "itemId": ObjectId(item[4]),
                    "itemCount": itemCount
                })
                db["orders"].update_one({
                    "clientId": userId,
                    "status": "koszyk"
                }, {
                    "$set": {
                        "itemList": itemList
                    }
                })
                top.destroy()
                messageString = "Dodano " + item[0] + " do koszyka"
                cont.show_frame(page)

def CreateOrderText(orderId):
    finalText = "OPIS ZAMÓWIENIA\n\nSKŁAD ZAMÓWIENIA\n"
    order = db["orders"].find_one({"_id": ObjectId(orderId)})
    itemList = order["itemList"]

    for itemInfo in itemList:
        item = db["items"].find_one({"_id": itemInfo["itemId"]})
        itemTotalPrice = item["price"] * itemInfo["itemCount"]
        entryText = "- " + str(round(itemTotalPrice, 2)) + "zł   " + str(itemInfo["itemCount"]) + "x" + \
                    str(round(item["price"], 2)) + "zł   " + item["name"] + "\n"
        finalText += entryText

    finalText += "\nCAŁKOWITY KOSZT ZAMÓWIENIA: " + str(order["totalPrice"]) + "zł"
    finalText += "\n\nMETODA PŁATNOŚCI: " + order["payment"]
    finalText += "\nSPOSÓB DOSTAWY: " + order["delivery"]+"\n"

    if order["delivery"] != "odbiór osobisty":
        adresDostawy = order["address"]
        finalText += "\n\nADRES DOSTAWY:\n"
        finalText += "Ulica: " + adresDostawy["street"] + "\n"
        finalText += "Numer domu: " + adresDostawy["number"] + "\n"
        if "apartment" in adresDostawy.keys():
            finalText += "Numer Mieszkania: " + adresDostawy["apartment"] + "\n"
        finalText += "Miasto: " + adresDostawy["city"] + "\n"
        finalText += "Kod pocztowy: " + adresDostawy["ZIP"] + "\n"

    return finalText


def setEditUser(userId):
    global editedUserId
    editedUserId = userId


def updateCartsAndFavourites(itemId):
    itemId = ObjectId(itemId)
    clients = db["users"].find({"type": "klient"})
    for c in clients:
        clientCart = db["orders"].find_one({"clientId": c["_id"], "status": "koszyk"})
        favourites = c["favourite"]
        for i in range(len(favourites)):
            if favourites[i] == itemId:
                favourites.pop(i)
                db["users"].update_one({"_id": ObjectId(c["_id"])},{
                    "$set":{
                        "favourite": favourites
                    }
                })
                break
        cartItems = clientCart["itemList"]
        for i in range(len(cartItems)):
            if cartItems[i]["itemId"] == itemId:
                cartItems.pop(i)
                db["orders"].update_one({"_id": clientCart["_id"]},{
                    "$set":{
                        "itemList": cartItems
                    }
                })
                break


if __name__ == "__main__":
    app = App()
    app.mainloop()
