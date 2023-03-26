import SelectFiles
from Files import *

import customtkinter as Ctk
from customtkinter import *

class RenameFiles:
    def __init__(self, files):
        self.size = 24
        self.font = ("Ariel", self.size)

        self.files = files
        self.window = CTk()
        self.window.title("Rename Files")

        self.FindEntry = None
        self.ReplaceEntry = None
        self.AddEntry = None
        self.text_mode = None
        self.FormatEntry = None
        self.CounterEntry = None
        self.counter = 0
        self.ExtEntry = None
        self.initialRun = True

        self.changesFileLabel = None

        self.MainWindow()
        self.displayReplace()
        self.func = self.ReplaceMode

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
        self.window.mainloop()

    def DisplayChoices(self, curr):

        Options = ["Replace Text", "Add Text", "Format Text", "Change Ext"]
        text_mode = CTkOptionMenu(master=self.window, values=Options, command=self.SelectMode, font=("Ariel", self.size),width = 200, dynamic_resizing = False)
        text_mode.set(curr)
        text_mode.grid(row=0, column=0,padx=10, pady=10, columnspan = 2, sticky = Ctk.W)

    def SelectMode(self, choice):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.DisplayChoices(choice)
        self.MainWindow(choice)

        if choice == "Replace Text":
            self.displayReplace()
            self.func = self.ReplaceMode
        elif choice == "Add Text":
            self.displayAdd()
            self.func = self.AddMode
        elif choice == "Format Text":
            self.displayFormat()
            self.func = self.FormatMode
        elif choice == "Change Ext":
            self.displayChangeExt()




    def MainWindow(self, curr = "Replace Text"):
        self.window.geometry("950x190")
        firstFileName = self.files[0].fullFileName
        fileFontSize = min(24, int(800 / len(firstFileName)))
        self.DisplayChoices(curr)

        originalLabel = CTkLabel(self.window, text = " Original: ", font = self.font)
        originalLabel.grid(row = 2, column = 0, sticky= Ctk.W)

        changesLabel = CTkLabel(self.window, text=" Changes: ", font=self.font)
        changesLabel.grid(row=3, column=0, sticky= Ctk.W)

        originalFileLabel = CTkLabel(self.window, text= firstFileName, font= ("Ariel", fileFontSize))
        originalFileLabel.grid(row=2, column=1, sticky= Ctk.W, columnspan = 2)

        self.changesFileLabel = CTkLabel(self.window, text= firstFileName, font= ("Ariel", fileFontSize))
        self.changesFileLabel.grid(row=3, column=1, sticky= Ctk.W, columnspan = 2)

        def preview():
            if (curr == "Format Text"):
                self.counter = int(self.CounterEntry.get())
            previewText = self.func(self.files[0].fileName) + self.files[0].ext
            previewFontSize = min(24, int(800 / len(previewText)))
            self.changesFileLabel.destroy()
            self.changesFileLabel = CTkLabel(self.window, text=previewText, font=("Ariel", previewFontSize))
            self.changesFileLabel.grid(row=3, column=1, sticky=Ctk.W, columnspan=2)

        previewButton = CTkButton(self.window, text = "Preview Changes", font = self.font, command = preview)
        previewButton.grid(row = 2, column = 3, columnspan = 2,padx=10, pady=10)

        def cancel(SecondRun = False):
            self.window.destroy()
            SelectFiles.SelectedFiles(SecondRun)
            quit()

        cancelButton = CTkButton(self.window, text="cancel", font=self.font, command = cancel)
        cancelButton.grid(row=3, column=3, padx=10)

        def rename():
            for file in self.files:
                fileName = file.fileName
                newFileName = self.func(fileName)
                file.rename(newFileName)
                print(fileName + " -> " + newFileName)
                Files.initial.append(fileName)
                Files.changes.append(newFileName)
            cancel(True)

        renameButton = CTkButton(self.window, text="rename", font=self.font, command= rename)
        renameButton.grid(row=3, column=4, padx=10)


    def displayReplace(self):
        FindLabel = CTkLabel(self.window, text="Find: ", font=self.font)
        FindLabel.grid(row=1, column=0)

        self.FindEntry = CTkEntry(self.window, font=self.font, width=250)
        self.FindEntry.grid(row=1, column=1, columnspan=2)

        ReplaceLabel = CTkLabel(self.window, text="  Replace with: ", font=self.font)
        ReplaceLabel.grid(row=1, column=3)

        self.ReplaceEntry = CTkEntry(self.window, font=self.font, width=250)
        self.ReplaceEntry.grid(row=1, column=4, columnspan=2)

    def ReplaceMode(self, fileName):
        FindText = self.FindEntry.get()
        ReplaceText = self.ReplaceEntry.get()
        return fileName.replace(FindText, ReplaceText, 1)

    def displayAdd(self):
        AddLabel = CTkLabel(master = self.window, text = "Text to add: ",font=self.font)
        AddLabel.grid(row = 1, column = 0)

        self.AddEntry = CTkEntry(master = self.window, font=self.font , width=250)
        self.AddEntry.grid(row=1, column=1, columnspan = 1)

        Options = ["after name", "before name"]
        self.text_mode = CTkOptionMenu(master=self.window, values=Options, font=("Ariel", self.size), width = 180, dynamic_resizing = False)
        self.text_mode.set("after name")
        self.text_mode.grid(row=1, column=2, columnspan = 2, padx = 10)

    def AddMode(self, fileName):
        placement = self.text_mode.get()
        if placement == "after name":
            return fileName + self.AddEntry.get()
        else:
            return self.AddEntry.get() + fileName

    def displayFormat(self):

        self.initialRun = True
        formatText = CTkLabel(master=self.window, text=" Format text:", font= self.font)
        formatText.grid(row=1, column=0)

        self.FormatEntry = CTkEntry(master=self.window, font=self.font, width=250)
        self.FormatEntry.grid(row=1, column=1, columnspan = 2)

        CounterText = CTkLabel(master=self.window, text=" Start numbers at:", font = self.font)
        CounterText.grid(row=1, column=3)

        self.CounterEntry = CTkEntry(master=self.window, font= self.font, width=100)
        self.CounterEntry.grid(row=1, column=4)

    def FormatMode(self, filename):
        if self.initialRun:
            self.counter = int(self.CounterEntry.get())
            self.initialRun = False

        newText = self.FormatEntry.get()
        self.counter += 1

        return newText + str(self.counter -1 )

    def displayChangeExt(self):
        self.window.geometry("500x190")
        for widget in self.window.winfo_children():
            widget.destroy()
        self.DisplayChoices("Change Ext")

        ExtLabel = CTkLabel(self.window, text="New extension: ", font=self.font)
        ExtLabel.grid(row=1, column=0)

        self.ExtEntry = CTkEntry(self.window, font=self.font, width=250)
        self.ExtEntry.insert(0, ".")
        self.ExtEntry.grid(row=1, column=1, columnspan=2)


        CurrExt = CTkLabel(master = self.window, text = "Current Extension: ",font=self.font)
        CurrExt.grid(row = 2, column = 0, padx = 10, pady = 10)
        CurrExtLabel = CTkLabel(master = self.window, text = self.files[0].ext, font=self.font)
        CurrExtLabel.grid(row=2, column=1, pady = 10)

        def cancel(SecondRun = False):
            self.window.destroy()
            SelectFiles.SelectedFiles(SecondRun)
            quit()

        cancelButton = CTkButton(self.window, text="cancel", font=self.font, command = cancel)
        cancelButton.grid(row=3, column=0, padx=10)

        def rename():
            for file in self.files:
                file.changeExt(self.ExtEntry.get())
            cancel(True)

        renameButton = CTkButton(self.window, text="rename", font=self.font, command= rename)
        renameButton.grid(row=3, column=1, padx=10)