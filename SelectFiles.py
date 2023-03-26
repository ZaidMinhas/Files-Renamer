from RenameFiles import *
from customtkinter import *
from Files import *

class SelectedFiles:
    def __init__(self, secondRun = False):
        #Window set
        set_appearance_mode("dark")
        set_default_color_theme("blue")
        self.result = ()
        self.window = CTk()
        self.window.title("Select Files")
        self.size = 24
        CTkLabel(master = self.window, text = "").grid(row = 0, column = 0)
        self.Error = CTkLabel(master = self.window, text = "", font=("Ariel" , self.size))
        self.Error.grid(row=2, column=0, columnspan=2)
        self.label = CTkLabel(master = self.window, text="Select files to be renamed: ", font=("Ariel", self.size))
        self.label.grid(row=1, column=0)
        self.window.geometry("435x150")
        self.select = CTkButton(master = self.window, text="Browse", font=("Ariel", self.size), command=self.Select)
        self.select.grid(row=1, column=1)
        if secondRun:
            self.revert = CTkButton(self.window, text="Revert", font=("Ariel", self.size), fg_color="#b50000", command = Files.revert)
            self.revert.grid(row=3, column=0, columnspan=2)
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
        self.window.bind('<Return>', lambda event: self.Select())

        self.window.mainloop()



    def Select(self):
        #Open file dialog box and select files
        f = filedialog.askopenfilenames()
        f = [Files(i) for i in f]

        if len(f) == 0:
            self.displayError("No files selected")
        elif self.MultipleFileTypes(f):
            self.displayError("Selected multiple file types")
        else:
            self.window.destroy()
            Files.initial = []
            Files.changes = []
            RenameFiles(f)
            quit()


    def displayError(self, msg=""):
        #Displays the error from selecting files
        ERROR = CTkLabel(self.window, text=msg, font=("Ariel", self.size), fg_color= "#b50000")
        ERROR.grid(row=2, column=0, columnspan=2, pady = 10)

    def MultipleFileTypes(self, f):
        ext = []
        for i in f:
            ext.append(i.ext)
        return len(set(ext)) > 1

    def getFiles(self):
        return self.result