import os

class TokenHandler:

    def __init__(self):
        self.filename = "tokens.txt"

        if os.path.isfile(self.filename):   # Boolean
            pass
        else:
            open("tokens.txt", "w").close()  # Gaurentees creation of tokens.txt if it is not created
    
    def write(self, token:str, mode:str="a+")  ->  None:
        keysfile = open(self.filename, mode)    # Opens file in appending mode
        keysfile.writelines(token + "\n")
        keysfile.close()

    def writelines(self, data:list=None, mode:str="a+")    ->  None:
        keysfile = open(self.filename, mode)
        for item in data:
            keysfile.write(item + "\n")
        keysfile.close()

    def read(self)    ->  list:
        keysfile = open(self.filename, "r") # Opens the file in read mode
        foo = keysfile.readlines()
        keysfile.close()
        return [x.replace("\n", "") for x in foo]

    def deleteValue(self, value:str=None)   ->  None:
        '''
Deletes all instances of a value in the file.
        '''
        data = self.read()
        for x in range(len(data)):
            try:
                data.remove(value)
            except ValueError:
                break
        self.writelines(data=data, mode="w")