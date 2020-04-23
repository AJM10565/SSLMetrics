import requests
import sys

print("Hello, World!")
cliArg1 = sys.argv[1]
print("Your first command line argument is: ")
print(cliArg1)
result = requests.get('https://jsonplaceholder.typicode.com/todos/1')
print(result.json())
