# SSLMetrics

## How It Works
Using the [GitHub API](https://developer.github.com/v3/) we gather information about a repository, and use [pandas](https://pandas.pydata.org/) to display the information.

## Module Development
### How to use the module template
First, create a folder for your module (following the file structure of this template, `module_template` would be that folder). Then, create another folder called `code` within that folder. Inside the `code` folder, place all of your Python code for your module. For each library you import, add it to a file called `requirements.txt` within the `code` folder. Lastly, copy the `Dockerfile` from this template into the folder of the module itself.

### How to run the module
`cd` into the module folder you created, then (in your Docker terminal) run `docker build -t your_module .`

This will create a Docker image with the name your_module. To run a container of that image, run `docker run your_module [cliArgs]`, where `[cliArgs]` are optional command line arguments passed directly to the entry file. Note that all modules must begin execution at a script named in the Dockerfile as `app.py` - feel free to change the name in the Dockerfile of your own module to fit this requirement, or simply name your entry script `app.py` as well.

### Instructions to make the example work
In your Docker terminal, `cd` into the `module_template` folder, run `docker build -t template .` . When that finishes, run `docker run template word` , where `word` is a word of your choice to print, showing how to pass command line arguments through Docker to Python. The script also prints the results of a basic HTTP GET request, to utilize the requests library that serves as a placeholder in the example `requirements.txt` . The result should look like this:

        Hello, World!
        Your first command line argument is:
        word
        {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}


    
   
