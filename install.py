import subprocess
import os
print("Installtion process has started and it takes some time to be proccessed")
subprocess.run(["pip", "install", "-r", "requirements.txt"])
print("Installed successfully. Now run main.py to execture the program")
