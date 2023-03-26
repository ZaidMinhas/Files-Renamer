import os
class Files:
    initial = []
    changes = []
    path = ""
    ext = ""
    def __init__(self, file):
        self.file = file
        self.path = os.path.dirname(self.file) + "/"
        self.fullFileName = os.path.basename(self.file)
        self.fileName = os.path.splitext(self.fullFileName)[0]
        self.ext = os.path.splitext(self.fullFileName)[1]
        Files.path = self.path
        Files.ext = self.ext

    def updateFileName(self, newFileName):
        return self.path + newFileName + self.ext

    def rename(self, newFileName):
        os.rename(self.file, self.updateFileName(newFileName))

    def changeExt(self, ext):
        os.rename(self.file, self.path + self.fileName + ext)

    @staticmethod
    def revert():
        for i in range(len(Files.initial)):
            os.rename(Files.path + Files.changes[i] + Files.ext, Files.path + Files.initial[i] + Files.ext)
            print(Files.changes[i] + " -> " +  Files.initial[i])
            Files.changes, Files.initial = Files.initial, Files.changes