import subprocess
import platform

# Get operating system of current platform
host_os = platform.system()

if host_os == "Darwin":
    print("I'm a Mac!")
elif host_os == "Linux":
    print("I run Linux!")
elif host_os == "Windows":
    subprocess.call("./data-vis-win32-x64/data-vis.exe")
