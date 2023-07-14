import os
import re


class Rename:
    def __init__(self, full_files):
        self.full_file_names  = [os.path.basename(file) for file in full_files]
        fileRE = re.compile(r"(.+)\.(.+)$")

        fileList = [fileRE.findall(file)[0] for file in self.full_file_names]
        self.file_names, file_extensions = zip(*fileList)

        # Check if there are multiple extensions
        self.ext = list(set(file_extensions))
        if len(self.ext) > 1:
            raise TooManyExtensions(self.ext)

        # Set extension and full file names
        self.ext = self.ext[0]


        #Original file path
        self.path = os.path.dirname(full_files[0])
        #File names with extension

        #file names without extension

        #New file name with extension
        self.new_full_file_names = []


    def ReplaceText(self, file, find, replace):
        new_file = file.replace(find, replace)

        return f"{new_file}.{self.ext}"

    def AddText(self, file, text, placement):
        new_file = ""
        if (placement):
            new_file = file + text
        else:
            new_file = text + file
        return f"{new_file}.{self.ext}"


    def FormatText(self, file, text, number):
        return f"{text}{number}.{self.ext}"

    def ChangeExt(self, file, new_ext):
        return f"{file}.{new_ext}"

    def RenameAll(self, TextMode, *args):
        self.new_full_file_names = []
        if (TextMode == self.FormatText):
            text = args[0]
            number = args[1]
            for file in self.file_names:
                new_name = TextMode(file, text, number)
                number += 1
                self.new_full_file_names.append(new_name)
        else:
            for file in self.file_names:
                new_name = TextMode(file, *args)
                self.new_full_file_names.append(new_name)

    def Commit(self):
        for i in range(len(self.file_names)):
            os.rename(self.path  +"/" + self.full_file_names[i], self.path  +"/" + self.new_full_file_names[i])

    def Revert(self):
        for i in range(len(self.file_names)):
            os.rename(self.path +"/" + self.new_full_file_names[i], self.path +"/" + self.full_file_names[i])


class TooManyExtensions(Exception):
    def __init__(self, ext):
        self.ext = ext
        super().__init__("Too many extensions found: ", self.ext)
