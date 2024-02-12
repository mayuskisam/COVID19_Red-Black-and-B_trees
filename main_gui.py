from tkinter import *
from tkinter import ttk


def mainGui(root, tree):

    # functions to update date label
    def updateDay(day):
        dayStringMain.set(day)
        updateDateLabels(None)

    def updateDateLabels(event):
        # if year, month, day are chosen, update date labels
        if (
            yearStringMain.get() != ""
            and monthStringMain.get() != ""
            and dayStringMain.get() != ""
        ):
            # update date labels
            dateLabel.config(
                text="Date: {} {}, {}".format(
                    monthStringMain.get(), dayStringMain.get(), yearStringMain.get()
                )
            )
            # update data
            updateData()

    # functions to update data
    def updateData(event=None):
        if (
            yearStringMain.get() != ""
            and monthStringMain.get() != ""
            and dayStringMain.get() != ""
            and countryStringMain.get() != ""
        ):
            date = dateFormat()
            country = countryStringMain.get()
            cases = tree.search(tree.root, country, date)
            if cases != None:
                casesLabel.configure(text="Cases: {}".format(cases))
            else:
                casesLabel.configure(
                    text="Cases: No data for this date & country")

    def dateFormat():  # format date to be used in tree
        match monthStringMain.get():
            case "January":
                month = "01"
            case "February":
                month = "02"
            case "March":
                month = "03"
            case "April":
                month = "04"
            case "May":
                month = "05"
            case "June":
                month = "06"
            case "July":
                month = "07"
            case "August":
                month = "08"
            case "September":
                month = "09"
            case "October":
                month = "10"
            case "November":
                month = "11"
            case "December":
                month = "12"
        return "{}-{}-{}".format(yearStringMain.get(), month, dayStringMain.get().zfill(2))

    # create grid layout
    rootFrame = ttk.Frame(root, padding="3 3 6 6")
    rootFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    leftFrame = ttk.Frame(rootFrame, padding="3 3 6 6")
    leftFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    leftFrameTop = ttk.Frame(leftFrame, padding="3 3 6 6")
    leftFrameTop.grid(column=0, row=0, sticky=(N, W, E, S))
    leftFrameBottom = ttk.Frame(leftFrame, padding="3 3 6 6")
    leftFrameBottom.grid(column=0, row=1, sticky=(N, W, E, S))

    rightFrame = ttk.Frame(rootFrame, padding="3 3 6 6")
    rightFrame.grid(column=2, row=0, sticky=(N, W, E, S))
    rightFrameTop = ttk.Frame(rightFrame, padding="3 3 6 6")
    rightFrameTop.grid(column=0, row=0, sticky=(N, W, E))
    rightFrameBottom = ttk.Frame(rightFrame, padding="3 3 6 6")
    rightFrameBottom.grid(column=0, row=2, sticky=(S, W, E))
    rightFrame.rowconfigure(2, weight=1)

    # left frame
    # buttons for calendar
    dayStringMain = StringVar()
    dayButtons = []
    for i in range(5):
        for j in range(7):
            if i * 7 + j < 31:
                dayButtons.append(
                    ttk.Button(
                        leftFrameTop,
                        text="{}".format(i * 7 + j + 1),
                        command=lambda day=i * 7 + j + 1: updateDay(day),
                    )
                )
                dayButtons[i * 7 + j].grid(column=j, row=i)

    # bottom left frame
    # month
    ttk.Label(leftFrameBottom, text="Month: ").grid(column=0, row=0)
    monthStringMain = StringVar()
    monthPicker = ttk.Combobox(
        leftFrameBottom,
        values=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        textvariable=monthStringMain,
    )
    monthPicker.grid(column=1, row=0)
    monthPicker.bind("<<ComboboxSelected>>", updateDateLabels)
    monthPicker.state(["readonly"])
    # year
    ttk.Label(leftFrameBottom, text="Year: ").grid(column=0, row=1)
    yearStringMain = StringVar()
    yearPicker = ttk.Combobox(
        leftFrameBottom, values=["2020", "2021", "2022"], textvariable=yearStringMain
    )
    yearPicker.grid(column=1, row=1)
    yearPicker.bind("<<ComboboxSelected>>", updateDateLabels)
    yearPicker.state(["readonly"])

    # left & right separator
    ttk.Separator(rootFrame, orient=VERTICAL).grid(
        column=1, row=0, sticky=(N, S))

    # right frame
    # country picker
    ttk.Label(rightFrameTop, text="Country: ").grid(column=0, row=0)
    countryStringMain = StringVar()
    countryPicker = ttk.Combobox(
        rightFrameTop,
        values=tree.getCountries(tree.root),
        textvariable=countryStringMain,
    )
    countryPicker.grid(column=1, row=0)
    countryPicker.bind("<<ComboboxSelected>>", updateData)
    countryPicker.state(["readonly"])

    # separator
    ttk.Separator(rightFrame, orient=HORIZONTAL).grid(
        column=0, row=1, columnspan=2, sticky=(E, W)
    )

    # data labels
    dateLabel = ttk.Label(rightFrameBottom, text="Date: Not Chosen")
    dateLabel.grid(column=0, row=0)
    casesLabel = ttk.Label(rightFrameBottom, text="Total Cases: ")
    casesLabel.grid(column=0, row=1)
