import sys

class Count:
    '''
This is a series of metrics meant to count the number of blank lines, comments, code lines, and charachters in a file.
    '''
    def __init__(self, filename:str=None)   ->  None:
        '''
Initalizes the class and reads the data from a file into a list.\n
:param filename: The name of the file to be opened and read from.
        '''
        self.file = open(filename, "r")
        self.fileData = self.file.readlines()

    def close_File(self) ->  None:
        '''
Safely closes the file that is currently opened.
        '''
        self.file.close()

    def count_BlankLines(self)   ->  int:
        '''
Counts the number of blank lines in a file.\n
A blank line is a line that only contains the \\n charachter.\n
:returns int: This is the total number of blank lines in the file.
        '''
        count = 0
        for x in self.fileData:
            if x == "\n":
                count += 1
        return count

    def count_Comments(self, openingCommentMark:str=None, closingCommentMark:str=None)   ->  int:
        '''
Counts the number of comments in a file.\n
This could also be repurposed to count the number of lines that start and end with a set of charachters or contain a set of charachters.\n
:param openingCommentMark: A required parameter that indicates what the initial comment mark looks like.\n
:param closingCommentMark: An optional parameter that indicated what the end comment mark looks like.\n
:return int: This is the total number of comments in the file. 
        '''
        # Test for the required param
        try:
            len_OCM = len(openingCommentMark)
        except TypeError:
            print("There needs to be an openingCommentMark arguement.")
            sys.exit()
        # Starts parsing
        count = 0
        # Parsing for one mark
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
        # Parsing for two marks
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

    def count_CountCodeLines(self)  ->  int:
        '''
Counts the number of code lines in a file.\n
A code line is a line that contains more than the \\n charachter.\n
:returns int: This is the total number of blank lines in the file.
        '''
        count = 0
        for x in self.fileData:
            if x != "\n":
                count += 1
        return count

    def count_CountCharachters(self)    ->  int:
        '''
Counts the number of charachters in a file.\n
A charachter is a line that contains more than the \\n charachter.\n
:returns int: This is the total number of blank lines in the file.
        '''
        count = 0
        for x in self.fileData:
            if x !="\n":
                try:
                    count += len(x[0:x.index("\n")])
                except ValueError:
                    count += len(x)
        return count

    def set_File(self, filename:str=None)   ->  None:
        '''
Opens a new file and reads the data from it.\n
:param filename: The name of the file to be opened and read from.
        '''
        self.file = open(filename, "r")
        self.fileData = self.file.readlines()
    
    def set_FileData(self)  ->  None:
        '''
Reads the data from the currently opened file.
        '''
        self.fileData = self.file.readlines()

c = Count(filename="test.txt")
print("Comments: " + str(c.count_Comments(openingCommentMark="//")))
print("Blank Lines: " + str(c.count_BlankLines()))
print("Code Lines: " + str(c.count_CountCodeLines()))
print("Chars:" + str(c.count_CountCharachters()))
