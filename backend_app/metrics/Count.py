from _io import TextIOWrapper
import sys

class Count:
    def __init__(self, file:str=None):
        self.file = open(file, "r")
        self.fileData = self.file.readlines()

    def close_File(self) ->  None:
        self.file.close()

    def count_BlankLines(self)   ->  int:
        count = 0
        for x in self.fileData:
            if x == "\n":
                count += 1
        return count

    def count_Comments(self, openingCommentMark:str=None, closingCommentMark:str=None)   ->  int:
        try:
            len_OCM = len(openingCommentMark)
        except TypeError:
            print("There needs to be an openingCommentMark arguement.")
            sys.exit()
        count = 0
        if closingCommentMark is None:
            for x in self.fileData:
                x = x.strip()
                if x[0:len_OCM] == openingCommentMark:  # Finds the comment mark assuming that it is the first charachter(s) of the line
                    count += 1
                else:
                    try:
                        x.index(openingCommentMark) # Finds the comment mark even if it is not the first charachter(s) in the line
                        count += 1
                    except ValueError:
                        pass
        else:
            for x in range(len(self.fileData)):
                foo = self.fileData[x].strip()
                if foo[0:len_OCM] == openingCommentMark:
                    bar = x # Stores the current index to avoid finding previous closingCommentMark(s)
                    while bar < len(self.fileData):
                        temp = self.fileData[bar].strip()
                        try:
                            temp.index(closingCommentMark)
                            count += 1
                            break
                        except ValueError:
                            bar += 1
        return count

    def set_File(self, file:str=None)   ->  None:
        self.file = open(file, "r")
        self.fileData = self.file.readlines()
    
# class CountLines:

#     def __init__(self):
#         pass

# class CountCharachters:

c = Count(file="test.txt")
print(c.count_Comments(openingCommentMark="//"))