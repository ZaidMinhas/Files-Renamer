import customtkinter as ctk

class RenameFiles(ctk.CTk):
    def __init__(self, rename):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.geometry("500x150+300+450")
        self.title("Rename File")

        self.rename = rename
        self.first_file = rename.file_names[0]

        self.TopMenu = TopMenu(self)
        self.TopMenu.pack(fill = "x",padx = 5, pady = 5)

        self.ReplaceFrame = ReplaceFrame(self)
        self.AddFrame = AddFrame(self)
        self.FormatFrame = FormatFrame(self)
        self.ChangeExtFrame = ChangeExtFrame(self, self.rename.ext)


        self.InputFrame = self.ReplaceFrame
        self.InputFrame.pack(fill = "x", padx = 5, pady = 5, expand = True)

        self.RenameMode = rename.ReplaceText

        self.BottomMenu = BottomMenu(self)
        self.BottomMenu.pack(side = "bottom", fill="x", padx=5, pady=5)

        self.mainloop()

    def Rename(self):
        args = self.InputFrame.getArgs()
        self.rename.RenameAll(self.RenameMode, *args)
        self.rename.Commit()
        self.destroy()



    def UpdatePreview(self):
        args = self.InputFrame.getArgs()
        self.rename.RenameAll(self.RenameMode, *args)

        old_names = self.rename.full_file_names
        new_names = self.rename.new_full_file_names

        preview_window = ctk.CTkToplevel()

        preview_window.title("Preview")
        preview_window.geometry("300x300")

        old_frame = ctk.CTkFrame(preview_window)
        new_frame = ctk.CTkFrame(preview_window)
        for i in range(len(old_names)):

            ctk.CTkLabel(old_frame, text = old_names[i]).pack(padx = 10)
            ctk.CTkLabel(new_frame, text = new_names[i]).pack(padx = 10)


        old_frame.pack(side = "left", fill = "y")
        new_frame.pack(side="left", fill="y")


    def ChangeFrame(self, text_mode):

        self.InputFrame.pack_forget()

        if (text_mode == "Replace Text"):
            self.InputFrame = self.ReplaceFrame
            self.RenameMode = self.rename.ReplaceText
        elif (text_mode == "Add Text"):
            self.InputFrame = self.AddFrame
            self.RenameMode = self.rename.AddText
        elif (text_mode == "Format Text"):
            self.InputFrame = self.FormatFrame
            self.RenameMode = self.rename.FormatText
        elif (text_mode == "Change Extension"):
            self.InputFrame = self.ChangeExtFrame
            self.RenameMode = self.rename.ChangeExt

        self.InputFrame.pack(fill = "x", padx = 5, pady = 5, expand = True)

class TopMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        Options = ["Replace Text", "Add Text", "Format Text", "Change Extension"]
        self.option_var = ctk.StringVar(value= Options[0])

        mode_menu = ctk.CTkOptionMenu(self,
                                      command= parent.ChangeFrame,
                                      variable=self.option_var,
                                      width=240,
                                      values=Options)

        mode_menu.pack(side="left", fill="both")

    def getMode(self):
        return self.option_var.get()

class ReplaceFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.replace_text = ctk.StringVar()
        self.find_text = ctk.StringVar()


        ctk.CTkLabel(self, text="Find").pack(side="left")
        ctk.CTkEntry(self, textvariable=self.find_text, width=150).pack(side="left", padx=10)
        ctk.CTkLabel(self, text="Replace with").pack(side="left")
        ctk.CTkEntry(self, textvariable=self.replace_text, width=150).pack(side="left", padx=10)

    def getArgs(self):
        return [self.find_text.get(), self.replace_text.get()]

class AddFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.Options = ["after name", "before name"]

        self.add_text = ctk.StringVar()
        self.pos_var = ctk.StringVar(value=self.Options[0])

        ctk.CTkLabel(self, text="Text to add").pack(side="left")
        ctk.CTkEntry(self, textvariable=self.add_text, width=150).pack(side="left", padx=10)

        add_pos = ctk.CTkOptionMenu(self, variable=self.pos_var, values=self.Options)

        add_pos.pack(side="left")

    def getArgs(self):
        self.pos_bool = self.pos_var.get() == self.Options[0]
        return [self.add_text.get(), self.pos_bool]

class FormatFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.format_text = ctk.StringVar()
        self.start_num = ctk.IntVar()

        ctk.CTkLabel(self, text=" Format text").pack(side="left")
        ctk.CTkEntry(self,textvariable= self.format_text, width=150).pack(side="left", padx=10)
        ctk.CTkLabel(self, text=" Start numbers at").pack(side="left")
        ctk.CTkEntry(self,textvariable= self.start_num,  width=50).pack(side="left", padx=10)

    def getArgs(self):
        return [self.format_text.get(), self.start_num.get()]

class ChangeExtFrame(ctk.CTkFrame):
    def __init__(self, parent, ext):
        super().__init__(parent)


        self.ext_text = ctk.StringVar()

        ctk.CTkLabel(self, text="New extension").pack(side="left")
        ctk.CTkEntry(self,textvariable= self.ext_text ,width=100).pack(side="left", padx=10)
        ctk.CTkLabel(self, text="Current extension").pack(side="left")
        ctk.CTkLabel(self, text=f".{ext}").pack(side="left", padx=10)

    def getArgs(self):
        return [self.ext_text.get()]

class BottomMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkButton(self, text = "Preview Changes", command = parent.UpdatePreview).pack(side = "left")
        # ctk.CTkLabel(self, anchor= ctk.CENTER).pack(side = "left", fill = "x", expand = True)
        ctk.CTkButton(self, text="Rename", command = parent.Rename).pack(side="right")
        ctk.CTkButton(self, text = "Cancel", command= lambda : parent.destroy()).pack(side = "right",padx = 10)
