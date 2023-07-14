import customtkinter as ctk
from Rename import *
from RenameFiles import RenameFiles


class SelectFiles(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.font = ctk.CTkFont(family="Ariel", size= 20)
        self.geometry("180x120+300+450")
        self.title("")
        self.files = []
        self.widgets()

        self.mainloop()

    def widgets(self):

        ctk.CTkLabel(self, text = "Select Files", font = self.font).pack(pady = 5)
        ctk.CTkButton(self, text = "Browse", font = self.font, command= self.select_files).pack()

    def select_files(self):
        full_files = ctk.filedialog.askopenfilenames()
        if not len(full_files):
            return 0
        try:
            rename = Rename(full_files)
        except TooManyExtensions:
            ctk.CTkLabel(self, text="Too many file types", font=self.font , fg_color= "#b50000").pack(pady = 5)
        else:
            self.destroy()
            RenameFiles(rename)


