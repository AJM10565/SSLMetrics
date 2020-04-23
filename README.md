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
        
        
### File sharing from Docker containers to host machine/other Docker containers (Windows)
To share files between your computer and your Docker containers, you need to create a volume. This should be pretty simple on *nix machines - I haven't had a chance to test on Mac/Linux, but I have been able to make it work on Windows, which is a more complicated process.

First, assuming you are not on an enterprise version of Windows and therefore you are using Docker Toolbox with Oracle VirtualBox, you will need to create a "Shared Folder".

I suggest following this tutorial and changing all instances of "Divio" in the commands to "metrics-vol" or something else you recognize: http://support.divio.com/en/articles/646695-how-to-use-a-directory-outside-c-users-with-docker-toolbox-docker-for-windows

The second part of this process, as mentioned in the tutorial, is permanently mounting the new shared folder in your default Docker machine. The tutorial provides good instructions on how to do this, and I will note that one way to edit the `profile` document is to use the default Linux `echo` command. First do a `sudo su` to give yourself proper permissions, then run `echo -e '\nsudo mkdir /metrics-vol\nsudo mount -t vboxsf -o uid=1000,gid=50 metrics-vol /metrics-vol' >> profile`.

After following the tutorial above as described, you should be able to read and write files in the shared folder you set up on your host machine from your Docker containers at the path `/metrics-vol`, so long as you mount a volume when you run the container. This command should look like `docker run -v /metrics-vol:/metrics-vol image-name command_line_argument`
I've included some test code in module_template/app.py that is currently commented out - if you correctly add a shared folder on your host machine, mount the folder on your default Docker machine, and mount it as a volume when you run the container (after building the image with the lines uncommented), it should write your command line argument
to a file called `voltest.txt` that exists in your shared folder on your host machine.

### File sharing from Docker containers to host machine/other Docker containers (Mac)

docker volume create metrics

docker build . -t name_of_image

docker run -v metrics:/metrics <name_of_image> github.com/owner/repo_name

#### To get data from inside volume after docker is dead

get docker id:

`docker container ls -a`

copy data:

`docker cp id:/metrics /path/to/file/on/host`

#### Running FE Flask Server to Display Data

`docker run -v metrics:/metrics -p 5000:5000 <name_of_image>`

#### Running the script to run everything

To run the scripts, run the following commands while in the top SSLMetrics directory:
`
chmod +x ./all_metrics.sh

chmod +x ./Commits/metrics.sh

chmod +x ./Issues/metrics.sh

chmod +x ./Lines_Of_Code_Num_Of_Chars/metrics.sh

chmod +x ./Issue_Spoilage/metrics.sh

chmod +x ./Defect_Density/metrics.sh

./all_metrics.sh github.com/<owner>/<repo_name> <api_token>
`
Note: the chmod commands need to be run only initially. After that, just run the all_metrics.sh script with the GitHub repo as the command line argument.
