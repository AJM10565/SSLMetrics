import subprocess
import platform

# Get operating system of current platform
host_os = platform.system()

if host_os is "Darwin":
    # Replace arg in following line with path to .app file on Mac
    # subprocess.call("")
    print("I'm a Mac!")
elif host_os is "Linux":
    # Replace arg in following line with path to executable file on Linux
    # subprocess.call("")
    print("I run Linux!")
else:
    subprocess.call("./data-vis-win32-x64/data-vis.exe")
