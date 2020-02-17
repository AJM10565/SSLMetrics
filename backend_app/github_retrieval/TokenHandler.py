class TokenHandler:

    def __init__(self):
        self.filename = "tokens.txt"
    
    def writer(self, tag:str)  ->  None:
        keysfile = open(self.filename, "a+")    # Opens file in appending mode
        keysfile.writelines(tag + "\n")
        keysfile.close()

    def reader(self)    ->  list:
        keysfile = open(self.filename, "r") # Opens the file in read mode
        foo = keysfile.readlines()
        keysfile.close()
        return [x.replace("\n", "") for x in foo]