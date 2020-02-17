class TokenHandler:

    def __init__(self):
        self.filename = "tokens.txt"
        open("tokens.txt", "w").close()  # Gaurentees creation of tokens.txt if it is not created
    
    def write(self, token:str)  ->  None:
        keysfile = open(self.filename, "a+")    # Opens file in appending mode
        keysfile.writelines(token + "\n")
        keysfile.close()

    def read(self)    ->  list:
        keysfile = open(self.filename, "r") # Opens the file in read mode
        foo = keysfile.readlines()
        keysfile.close()
        return [x.replace("\n", "") for x in foo]