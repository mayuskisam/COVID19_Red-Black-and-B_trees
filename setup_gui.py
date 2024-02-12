import time
import pandas as pd
from tkinter import *
from tkinter import ttk
import rb_tree
import b_tree
import main_gui


def setupGui():

    # main functions
    def insertIntoRbTree(n):  # insert n values into tree
        statusLabel.config(text="Working...", foreground="yellow4")
        root.update_idletasks()
        df = pd.read_csv("covid.csv")
        start = time.time()
        if 1 <= n < len(df):
            for i in range(n):
                rbTree.insert(
                    rbTree.root, df.iloc[i][2], df.iloc[i][4], df.iloc[i][0])
            end = time.time()
            statusLabel.config(
                text="Success! Completed in {} seconds".format(
                    round(end - start, 5)),
                foreground="green4",
            )
            updateCountries(rbTree)
            return rbTree
        else:
            statusLabel.config(text="Invalid value for n", foreground="red2")

    def insertIntoBTree(n):  # insert n values into tree
        statusLabel.config(text="Working...", foreground="yellow4")
        root.update_idletasks()
        df = pd.read_csv("covid.csv")
        start = time.time()
        if 1 <= n < len(df):
            for i in range(n):
                bTree.insert(
                    (df.iloc[i][4], (df.iloc[i][2], df.iloc[i][0])))
            end = time.time()
            statusLabel.config(
                text="Success! Completed in {} seconds".format(
                    round(end - start, 5)),
                foreground="green4",
            )
            updateCountries(bTree)
        else:
            statusLabel.config(text="Invalid value for n", foreground="red2")

    def updateCountries(tree):  # update the countries list
        countries = tree.getCountries(tree.root)
        if tree == rbTree:
            rbSearchCountryPicker["values"] = countries
        else:
            bSearchCountryPicker["values"] = countries

    def dateFormat(day, month, year):  # format date to be used in tree
        match month:
            case "Jan":
                month = "01"
            case "Feb":
                month = "02"
            case "Mar":
                month = "03"
            case "Apr":
                month = "04"
            case "May":
                month = "05"
            case "Jun":
                month = "06"
            case "Jul":
                month = "07"
            case "Aug":
                month = "08"
            case "Sep":
                month = "09"
            case "Oct":
                month = "10"
            case "Nov":
                month = "11"
            case "Dec":
                month = "12"
        return "{}-{}-{}".format(year, month, day)

    def searchTree(tree, country, date):  # search tree for cases
        statusLabel.config(text="Working...", foreground="yellow4")
        root.update_idletasks()
        start = time.time()
        cases = tree.search(tree.root, country, date)
        end = time.time()
        if cases != None:
            statusLabel.config(
                text="Success! Completed in {} seconds. Cases: {}".format(
                    round(end - start, 5), cases
                ),
                foreground="green4",
            )
        else:
            statusLabel.config(
                text="No data for this date & country", foreground="red2"
            )

    def openMainWindow(tree):
        mainRoot = Toplevel(root)
        mainRoot.title("Covid-19 Data")
        main_gui.mainGui(mainRoot, tree)
        mainRoot.mainloop()

    # root window
    root = Tk()
    root.title("Covid Data - Setup")
    root.minsize(600, 300)
    root.resizable(False, False)

    # initialize trees
    rbTree = rb_tree.rbTree()
    bTree = b_tree.bTree(3)

    # grid layout
    rootFrame = ttk.Frame(root, padding="3 3 6 6")
    rootFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # status
    statusFrame = ttk.Frame(rootFrame, padding="3 3 6 6")
    statusFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    statusLabelStatic = ttk.Label(statusFrame, text="Status: ")
    statusLabelStatic.grid(column=0, row=0)
    statusLabelStatic.config(font=("TkDefaultFont", 16, "bold"))
    statusLabel = ttk.Label(statusFrame, text="Ready")
    statusLabel.grid(column=1, row=0, sticky=(N, W, E, S))
    statusLabel.config(font=("TkDefaultFont", 16, "bold"))

    # separator
    ttk.Separator(rootFrame, orient=HORIZONTAL).grid(
        column=0, row=1, columnspan=7, pady=20, sticky=(W, E)
    )

    # rb tree
    rbFrame = ttk.Frame(rootFrame, padding="3 3 6 6")
    rbFrame.grid(column=0, row=2, sticky=(N, W, E, S))
    rbTitle = ttk.Label(rbFrame, text="Red Black Tree")
    rbTitle.grid(column=0, row=0, sticky=(N, W, E, S))
    rbTitle.config(font=("TkDefaultFont", 12, "bold"))
    # insert
    rbInsertLabel = ttk.Label(
        rbFrame, text="Number of nodes n to insert from data: ")
    rbInsertLabel.grid(column=0, row=1, sticky=(N, W, E, S))
    rbInsertNumberField = ttk.Entry(rbFrame, width=7)
    rbInsertNumberField.grid(column=1, row=1, sticky=(N, W, E, S))
    rbInsertNumberButton = ttk.Button(
        rbFrame,
        text="Insert",
        command=lambda: (
            insertIntoRbTree(
                int(rbInsertNumberField.get()))),
    )
    rbInsertNumberButton.grid(column=2, row=1, sticky=(N, W, E, S))
    # search
    ttk.Label(rbFrame, text="Search for node with country ").grid(
        column=0, row=2, sticky=(N, W, E, S)
    )
    rbCountryString = StringVar()
    rbSearchCountryPicker = ttk.Combobox(
        rbFrame, values=rbTree.getCountries(rbTree.root), textvariable=rbCountryString
    )
    rbSearchCountryPicker.grid(column=1, row=2, sticky=(N, W, E, S))
    rbSearchCountryPicker.state(["readonly"])
    ttk.Label(rbFrame, text=" and date ").grid(
        column=2, row=2, sticky=(N, W, E, S))
    rbDayString = StringVar()
    rbSearchDateDayPicker = ttk.Combobox(
        rbFrame, values=[*range(1, 32)], textvariable=rbDayString
    )
    rbSearchDateDayPicker.grid(column=3, row=2, sticky=(N, W, E, S))
    rbSearchDateDayPicker.state(["readonly"])
    rbSearchDateDayPicker.current(0)
    rbMonthString = StringVar()
    rbSearchDateMonthPicker = ttk.Combobox(
        rbFrame,
        values=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        textvariable=rbMonthString,
    )
    rbSearchDateMonthPicker.grid(column=4, row=2, sticky=(N, W, E, S))
    rbSearchDateMonthPicker.state(["readonly"])
    rbSearchDateMonthPicker.current(0)
    rbYearString = StringVar()
    rbSearchDateYearPicker = ttk.Combobox(
        rbFrame, values=[*range(2020, 2023)], textvariable=rbYearString
    )
    rbSearchDateYearPicker.grid(column=5, row=2, sticky=(N, W, E, S))
    rbSearchDateYearPicker.state(["readonly"])
    rbSearchDateYearPicker.current(0)
    rbSearchButton = ttk.Button(
        rbFrame,
        text="Search",
        command=lambda: searchTree(
            rbTree,
            rbCountryString.get(),
            dateFormat(
                rbDayString.get().zfill(2), rbMonthString.get(), rbYearString.get()
            ),
        ),
    )
    rbSearchButton.grid(column=6, row=2, sticky=(N, W, E, S))
    # traversals
    ttk.Label(rbFrame, text="Print traversals to console: ").grid(
        column=0, row=3, sticky=(N, W, E, S)
    )
    preorderButton = ttk.Button(
        rbFrame,
        text="Preorder Traversal",
        command=lambda: rbTree.preOrder(rbTree.root),
    )
    preorderButton.grid(column=1, row=3, sticky=(N, W, E, S))
    inorderButton = ttk.Button(
        rbFrame,
        text="Inorder Traversal",
        command=lambda: rbTree.inOrder(rbTree.root),
    )
    inorderButton.grid(column=2, row=3, sticky=(N, W, E, S))
    postorderButton = ttk.Button(
        rbFrame,
        text="Postorder Traversal",
        command=lambda: rbTree.postOrder(rbTree.root),
    )
    postorderButton.grid(column=3, row=3, sticky=(N, W, E, S))

    # separator
    ttk.Separator(rootFrame, orient=HORIZONTAL).grid(
        column=0, row=3, columnspan=7, pady=20, sticky=(N, W, E, S)
    )

    # b tree
    bFrame = ttk.Frame(rootFrame, padding="3 3 6 6")
    bFrame.grid(column=0, row=4, sticky=(N, W, E, S))
    bTitle = ttk.Label(bFrame, text="B Tree")
    bTitle.grid(column=0, row=0, sticky=(N, W, E, S))
    bTitle.config(font=("TkDefaultFont", 12, "bold"))
    # insert
    bInsertLabel = ttk.Label(
        bFrame, text="Number of nodes n to insert from data: ")
    bInsertLabel.grid(column=0, row=1, sticky=(N, W, E, S))
    bInsertNumberField = ttk.Entry(bFrame, width=7)
    bInsertNumberField.grid(column=1, row=1, sticky=(N, W, E, S))
    bInsertNumbebutton = ttk.Button(
        bFrame,
        text="Insert",
        command=lambda: (
            insertIntoBTree(
                int(bInsertNumberField.get()))),
    )
    bInsertNumbebutton.grid(column=2, row=1, sticky=(N, W, E, S))
    # search
    ttk.Label(bFrame, text="Search for node with country ").grid(
        column=0, row=2, sticky=(N, W, E, S)
    )
    bCountryString = StringVar()
    bSearchCountryPicker = ttk.Combobox(
        bFrame, values=bTree.getCountries(bTree.root), textvariable=bCountryString
    )
    bSearchCountryPicker.grid(column=1, row=2, sticky=(N, W, E, S))
    bSearchCountryPicker.state(["readonly"])
    ttk.Label(bFrame, text=" and date ").grid(
        column=2, row=2, sticky=(N, W, E, S))
    bDayString = StringVar()
    bSearchDateDayPicker = ttk.Combobox(
        bFrame, values=[*range(1, 32)], textvariable=bDayString
    )
    bSearchDateDayPicker.grid(column=3, row=2, sticky=(N, W, E, S))
    bSearchDateDayPicker.state(["readonly"])
    bSearchDateDayPicker.current(0)
    bMonthString = StringVar()
    bSearchDateMonthPicker = ttk.Combobox(
        bFrame,
        values=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        textvariable=bMonthString,
    )
    bSearchDateMonthPicker.grid(column=4, row=2, sticky=(N, W, E, S))
    bSearchDateMonthPicker.state(["readonly"])
    bSearchDateMonthPicker.current(0)
    bYearString = StringVar()
    bSearchDateYearPicker = ttk.Combobox(
        bFrame, values=[*range(2020, 2023)], textvariable=bYearString
    )
    bSearchDateYearPicker.grid(column=5, row=2, sticky=(N, W, E, S))
    bSearchDateYearPicker.state(["readonly"])
    bSearchDateYearPicker.current(0)
    bSearchButton = ttk.Button(
        bFrame,
        text="Search",
        command=lambda: searchTree(
            bTree,
            bCountryString.get(),
            dateFormat(
                bDayString.get().zfill(2), bMonthString.get(), bYearString.get()
            ),
        ),
    )
    bSearchButton.grid(column=6, row=2, sticky=(N, W, E, S))
    # traversals
    ttk.Label(bFrame, text="Print traversals to console: ").grid(
        column=0, row=3, sticky=(N, W, E, S)
    )
    preordebutton = ttk.Button(
        bFrame,
        text="Preorder Traversal",
        command=lambda: bTree.preOrder(bTree.root),
    )
    preordebutton.grid(column=1, row=3, sticky=(N, W, E, S))
    inordebutton = ttk.Button(
        bFrame,
        text="Inorder Traversal",
        command=lambda: bTree.inOrder(bTree.root),
    )
    inordebutton.grid(column=2, row=3, sticky=(N, W, E, S))
    postordebutton = ttk.Button(
        bFrame,
        text="Postorder Traversal",
        command=lambda: bTree.postOrder(bTree.root),
    )
    postordebutton.grid(column=3, row=3, sticky=(N, W, E, S))

    # separator
    ttk.Separator(rootFrame, orient=HORIZONTAL).grid(
        column=0, row=5, columnspan=7, pady=20, sticky=(N, W, E, S)
    )

    # buttons to go to calendar mode
    mainGuiButtonRb = ttk.Button(
        rootFrame,
        text="Go to calendar mode using Red-Black Tree",
        command=lambda: openMainWindow(rbTree),
    )
    mainGuiButtonRb.grid(column=0, row=6, columnspan=7, sticky=(N, W, E, S))
    mainGuiButtonB = ttk.Button(
        rootFrame,
        text="Go to calendar mode using B Tree",
        command=lambda: openMainWindow(bTree),
    )
    mainGuiButtonB.grid(column=0, row=7, columnspan=7, sticky=(N, W, E, S))

    # run main loop
    root.mainloop()
